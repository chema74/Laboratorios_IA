from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

RUTA_BASE = Path(__file__).resolve().parents[1]
RUTA_SRC = RUTA_BASE / "src"
if str(RUTA_SRC) not in sys.path:
    sys.path.insert(0, str(RUTA_SRC))

from laboratorio_privacidad_datos_sinteticos.anonimizador_demo import construir_dataset_anonimizado_demo
from laboratorio_privacidad_datos_sinteticos.cargador_contexto import cargar_contexto
from laboratorio_privacidad_datos_sinteticos.clasificador_sensibilidad import (
    NIVELES_SENSIBILIDAD,
    construir_clasificacion_sensibilidad,
    construir_inventario_datos,
)
from laboratorio_privacidad_datos_sinteticos.cli import _expediente, _resumen
from laboratorio_privacidad_datos_sinteticos.evaluador_riesgos import (
    ESTADOS_RIESGO,
    SEVERIDADES,
    construir_riesgos_privacidad_simulados,
)
from laboratorio_privacidad_datos_sinteticos.exportador import exportar_resultados
from laboratorio_privacidad_datos_sinteticos.matriz_permisos import NIVELES_ACCESO, construir_matriz_permisos_simulados
from laboratorio_privacidad_datos_sinteticos.minimizador_datos import construir_dataset_minimizado

OBLIGATORIOS_INVENTARIO = {
    "id_dato", "origen", "tipo_entidad", "campo", "valor_simulado_resumido", "nivel_sensibilidad_ficticia",
    "categoria_privacidad_simulada", "uso_previsto", "requiere_minimizacion", "requiere_anonimizacion",
    "requiere_revision_humana", "origen_simulado",
}


def _tmp_local(nombre: str) -> Path:
    base = RUTA_BASE / "tests" / ".tmp"
    base.mkdir(parents=True, exist_ok=True)
    ruta = base / nombre
    if ruta.exists():
        shutil.rmtree(ruta)
    ruta.mkdir(parents=True, exist_ok=True)
    return ruta


def _ctx() -> dict:
    return cargar_contexto("x", "y", "z", "w", "k", "m", "n", "o", "p", "q")


def test_inventario_y_reproducibilidad():
    ctx = _ctx()
    a = construir_inventario_datos(ctx, max_datos=80)
    b = construir_inventario_datos(ctx, max_datos=80)
    assert isinstance(a, list)
    assert a == b
    assert len(a) > 0


def test_inventario_campos_y_niveles_controlados():
    inv = construir_inventario_datos(_ctx(), max_datos=50)
    assert OBLIGATORIOS_INVENTARIO.issubset(inv[0].keys())
    assert all(x["nivel_sensibilidad_ficticia"] in NIVELES_SENSIBILIDAD for x in inv)


def test_clasificacion_matriz_y_nivel_acceso_controlado():
    inv = construir_inventario_datos(_ctx(), max_datos=60)
    clas = construir_clasificacion_sensibilidad(inv)
    mat = construir_matriz_permisos_simulados(inv)
    assert len(clas) > 0
    assert len(mat) > 0
    assert all(m["nivel_acceso"] in NIVELES_ACCESO for m in mat)


def test_minimizacion_y_anonimizacion_demo():
    inv = construir_inventario_datos(_ctx(), max_datos=60)
    mini = construir_dataset_minimizado(inv)
    ano = construir_dataset_anonimizado_demo(mini, seed=42)
    assert "datos_minimizados" in mini
    assert "datos_anonimizados_demo" in ano
    assert len(mini["datos_minimizados"]) > 0
    assert len(ano["datos_anonimizados_demo"]) > 0


def test_riesgos_controlados_y_revision_minimizacion():
    inv = construir_inventario_datos(_ctx(), max_datos=80)
    mat = construir_matriz_permisos_simulados(inv)
    riesgos = construir_riesgos_privacidad_simulados(inv, mat, _ctx())
    assert len(riesgos) > 0
    assert all(r["severidad"] in SEVERIDADES for r in riesgos)
    assert all(r["estado_riesgo"] in ESTADOS_RIESGO for r in riesgos)
    assert any(d["requiere_revision_humana"] or d["requiere_minimizacion"] for d in inv)


def test_exportaciones_completas():
    ctx = _ctx()
    inv = construir_inventario_datos(ctx, max_datos=70)
    clas = construir_clasificacion_sensibilidad(inv)
    mat = construir_matriz_permisos_simulados(inv)
    mini = construir_dataset_minimizado(inv)
    ano = construir_dataset_anonimizado_demo(mini, seed=42)
    riesgos = construir_riesgos_privacidad_simulados(inv, mat, ctx)
    resumen = _resumen(inv, riesgos, mat, {"entrada": "fallback"})
    expediente = _expediente(inv, clas, mat, riesgos, resumen)

    rutas = exportar_resultados(inv, clas, mat, mini, ano, riesgos, resumen, expediente, _tmp_local("out"))

    esperados = [
        "inventario_json", "inventario_csv", "clasificacion_json", "clasificacion_csv",
        "matriz_json", "matriz_csv", "minimizado_json", "anonimizado_json",
        "riesgos_json", "riesgos_csv", "resumen_json", "expediente_md",
    ]
    for clave in esperados:
        assert Path(rutas[clave]).exists()


def test_sin_api_claves_datos_reales_sin_agentes_sin_auditoria_legal_real_sin_anon_certificada():
    inv = construir_inventario_datos(_ctx(), max_datos=40)
    texto = json.dumps(inv, ensure_ascii=False).lower()
    assert "api_key" not in texto
    assert "token" not in texto
    assert "password" not in texto
    assert "ejecuta agentes reales" not in texto
    assert "auditoría legal real" not in texto
    assert "anonimización certificada" not in texto
