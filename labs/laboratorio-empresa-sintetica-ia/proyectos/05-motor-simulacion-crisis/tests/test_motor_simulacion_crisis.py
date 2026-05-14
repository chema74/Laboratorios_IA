from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

RUTA_BASE = Path(__file__).resolve().parents[1]
RUTA_SRC = RUTA_BASE / "src"
if str(RUTA_SRC) not in sys.path:
    sys.path.insert(0, str(RUTA_SRC))

from motor_simulacion_crisis.cargador_contexto import cargar_contexto
from motor_simulacion_crisis.catalogo_crisis import ESTADOS_CRISIS, SEVERIDADES
from motor_simulacion_crisis.evaluador_impacto import construir_expediente_markdown, construir_resumen_crisis
from motor_simulacion_crisis.exportador import exportar_resultados_crisis
from motor_simulacion_crisis.simulador import generar_linea_tiempo, simular_crisis


OBLIGATORIOS_CRISIS = {
    "id_crisis", "tipo_crisis", "titulo", "descripcion", "fecha_inicio", "fecha_fin_estimada", "severidad",
    "areas_afectadas", "entidades_afectadas", "eventos_relacionados", "documentos_relacionados", "escenarios_relacionados",
    "indicadores_impacto", "senales_tempranas", "decisiones_recomendadas", "riesgos_secundarios",
    "requiere_revision_humana", "estado_crisis", "origen_simulado",
}

OBLIGATORIOS_HITO = {
    "fecha", "id_crisis", "tipo_hito", "descripcion", "impacto_estimado", "decision_pendiente", "requiere_revision_humana",
}


def _tmp_local(nombre: str) -> Path:
    base = RUTA_BASE / "tests" / ".tmp"
    base.mkdir(parents=True, exist_ok=True)
    ruta = base / nombre
    if ruta.exists():
        shutil.rmtree(ruta)
    ruta.mkdir(parents=True, exist_ok=True)
    return ruta


def test_lista_crisis_y_reproducibilidad():
    ctx = cargar_contexto("x", "y", "z", "w")
    a = simular_crisis(ctx, seed=42, numero_crisis=5, dias=10)
    b = simular_crisis(ctx, seed=42, numero_crisis=5, dias=10)
    assert isinstance(a, list)
    assert a == b


def test_tipos_varios_y_campos_obligatorios():
    ctx = cargar_contexto("x", "y", "z", "w")
    crisis = simular_crisis(ctx, seed=1, numero_crisis=7, dias=10)
    tipos = {c["tipo_crisis"] for c in crisis}
    assert len(tipos) >= 4
    assert OBLIGATORIOS_CRISIS.issubset(crisis[0].keys())


def test_severidad_estado_controlados_y_revision_humana():
    ctx = cargar_contexto("x", "y", "z", "w")
    crisis = simular_crisis(ctx, seed=3, numero_crisis=8, dias=12)
    assert all(c["severidad"] in SEVERIDADES for c in crisis)
    assert all(c["estado_crisis"] in ESTADOS_CRISIS for c in crisis)
    assert any(c["requiere_revision_humana"] for c in crisis)


def test_crisis_privacidad_o_datos_corruptos():
    ctx = cargar_contexto("x", "y", "z", "w")
    crisis = simular_crisis(ctx, seed=5, numero_crisis=7, dias=10)
    tipos = {c["tipo_crisis"] for c in crisis}
    assert "incidente_privacidad" in tipos or "datos_corruptos" in tipos


def test_linea_tiempo_y_campos_hito():
    ctx = cargar_contexto("x", "y", "z", "w")
    crisis = simular_crisis(ctx, seed=6, numero_crisis=4, dias=8)
    linea = generar_linea_tiempo(crisis, seed=6)
    assert len(linea) > 0
    assert OBLIGATORIOS_HITO.issubset(linea[0].keys())


def test_exportaciones_completas():
    ctx = cargar_contexto("x", "y", "z", "w")
    crisis = simular_crisis(ctx, seed=8, numero_crisis=5, dias=10)
    linea = generar_linea_tiempo(crisis, seed=8)
    resumen = construir_resumen_crisis(crisis, linea, {"entrada_empresa": "x", "entrada_eventos": "y", "entrada_documentos": "z", "entrada_escenarios": "w"})
    expediente = construir_expediente_markdown(crisis, linea, resumen)
    salida = _tmp_local("out")

    rutas = exportar_resultados_crisis(crisis, linea, resumen, expediente, salida)
    assert Path(rutas["crisis_json"]).exists()
    assert Path(rutas["crisis_csv"]).exists()
    assert Path(rutas["linea_json"]).exists()
    assert Path(rutas["linea_csv"]).exists()
    assert Path(rutas["resumen_json"]).exists()
    assert Path(rutas["expediente_md"]).exists()


def test_fallback_sin_api_claves_datos_reales_sin_agentes_sin_prediccion():
    ctx = cargar_contexto("no1", "no2", "no3", "no4")
    crisis = simular_crisis(ctx, seed=10, numero_crisis=3, dias=6)
    texto = json.dumps(crisis, ensure_ascii=False).lower()
    assert "api_key" not in texto
    assert "token" not in texto
    assert "password" not in texto
    assert "predicción real" not in texto
    assert "ejecutar agentes reales" not in texto
