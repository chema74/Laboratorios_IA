from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

RUTA_BASE = Path(__file__).resolve().parents[1]
RUTA_SRC = RUTA_BASE / "src"
if str(RUTA_SRC) not in sys.path:
    sys.path.insert(0, str(RUTA_SRC))

from simulador_revision_humana.cargador_contexto import cargar_contexto
from simulador_revision_humana.catalogo_criterios import (
    ACCIONES_POSTERIORES_CONTROLADAS,
    DECISIONES_CONTROLADAS,
    ESTADOS_REGISTRO,
    NIVELES_CONFIANZA,
    ROLES_REVISORES,
)
from simulador_revision_humana.exportador import exportar_resultados_revision
from simulador_revision_humana.registro_decisiones import construir_expediente_revision_markdown, construir_resumen_revision_humana, generar_registro_decisiones
from simulador_revision_humana.simulador import simular_revisiones_humanas

OBLIGATORIOS_REV = {
    "id_revision", "tipo_elemento_revisado", "id_elemento_revisado", "titulo_elemento", "fecha_revision",
    "revisor_ficticio", "rol_revisor", "decision", "motivo_decision", "nivel_confianza_humana",
    "criterios_aplicados", "cambios_sugeridos", "accion_posterior", "requiere_segunda_revision", "trazabilidad", "origen_simulado",
}

OBLIGATORIOS_REG = {
    "id_registro", "id_revision", "fecha_registro", "decision", "accion_posterior",
    "resumen_trazabilidad", "impacto_simulado", "estado_registro",
}


def _tmp_local(nombre: str) -> Path:
    base = RUTA_BASE / "tests" / ".tmp"
    base.mkdir(parents=True, exist_ok=True)
    ruta = base / nombre
    if ruta.exists():
        shutil.rmtree(ruta)
    ruta.mkdir(parents=True, exist_ok=True)
    return ruta


def test_revisiones_lista_y_reproducibilidad():
    ctx = cargar_contexto("x", "y", "z", "w")
    a = simular_revisiones_humanas(ctx, seed=42, revisiones=20, porcentaje_escalado=25)
    b = simular_revisiones_humanas(ctx, seed=42, revisiones=20, porcentaje_escalado=25)
    assert isinstance(a, list)
    assert a == b


def test_varios_tipos_y_campos_obligatorios():
    ctx = cargar_contexto("x", "y", "z", "w")
    rev = simular_revisiones_humanas(ctx, seed=1, revisiones=16, porcentaje_escalado=20)
    tipos = {r["tipo_elemento_revisado"] for r in rev}
    assert len(tipos) >= 3
    assert OBLIGATORIOS_REV.issubset(rev[0].keys())


def test_valores_controlados_revision():
    ctx = cargar_contexto("x", "y", "z", "w")
    rev = simular_revisiones_humanas(ctx, seed=2, revisiones=20, porcentaje_escalado=30)
    assert all(r["decision"] in DECISIONES_CONTROLADAS for r in rev)
    assert all(r["accion_posterior"] in ACCIONES_POSTERIORES_CONTROLADAS for r in rev)
    assert all(r["nivel_confianza_humana"] in NIVELES_CONFIANZA for r in rev)
    assert all(r["rol_revisor"] in ROLES_REVISORES for r in rev)


def test_escaladas_o_segunda_revision():
    ctx = cargar_contexto("x", "y", "z", "w")
    rev = simular_revisiones_humanas(ctx, seed=3, revisiones=30, porcentaje_escalado=40)
    assert any(r["decision"] == "escalar" or r["requiere_segunda_revision"] for r in rev)


def test_registro_decisiones_y_campos_controlados():
    ctx = cargar_contexto("x", "y", "z", "w")
    rev = simular_revisiones_humanas(ctx, seed=4, revisiones=15, porcentaje_escalado=25)
    reg = generar_registro_decisiones(rev, seed=4)
    assert len(reg) == len(rev)
    assert OBLIGATORIOS_REG.issubset(reg[0].keys())
    assert all(r["estado_registro"] in ESTADOS_REGISTRO for r in reg)


def test_exportaciones_completas():
    ctx = cargar_contexto("x", "y", "z", "w")
    rev = simular_revisiones_humanas(ctx, seed=5, revisiones=12, porcentaje_escalado=20)
    reg = generar_registro_decisiones(rev, seed=5)
    resumen = construir_resumen_revision_humana(rev, reg, {"entrada_eventos": "x", "entrada_documentos": "y", "entrada_escenarios": "z", "entrada_crisis": "w"})
    expediente = construir_expediente_revision_markdown(rev, resumen)
    salida = _tmp_local("out")
    rutas = exportar_resultados_revision(rev, reg, resumen, expediente, salida)

    assert Path(rutas["revisiones_json"]).exists()
    assert Path(rutas["revisiones_csv"]).exists()
    assert Path(rutas["registro_json"]).exists()
    assert Path(rutas["registro_csv"]).exists()
    assert Path(rutas["resumen_json"]).exists()
    assert Path(rutas["expediente_md"]).exists()


def test_fallback_sin_api_claves_datos_reales_sin_agentes_sin_validacion_real():
    ctx = cargar_contexto("no1", "no2", "no3", "no4")
    rev = simular_revisiones_humanas(ctx, seed=6, revisiones=8, porcentaje_escalado=25)
    texto = json.dumps(rev, ensure_ascii=False).lower()
    assert "api_key" not in texto
    assert "token" not in texto
    assert "password" not in texto
    assert "ejecutar agentes reales" not in texto
    assert "validación profesional real" not in texto
