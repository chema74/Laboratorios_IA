from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

RUTA_BASE = Path(__file__).resolve().parents[1]
RUTA_SRC = RUTA_BASE / "src"
if str(RUTA_SRC) not in sys.path:
    sys.path.insert(0, str(RUTA_SRC))

from gemelo_digital_operativo_ligero.cargador_contexto import cargar_contexto
from gemelo_digital_operativo_ligero.evaluador_consecuencias import (
    construir_expediente_estado_operativo,
    construir_resumen_gemelo,
    generar_consecuencias_operativas,
)
from gemelo_digital_operativo_ligero.exportador import exportar_gemelo_digital
from gemelo_digital_operativo_ligero.motor_alertas import ESTADOS_ALERTA, SEVERIDADES
from gemelo_digital_operativo_ligero.simulador_estado import ESTADOS_DECISION, construir_estado_operativo

OBLIGATORIOS_ALERTA = {
    "id_alerta", "tipo_alerta", "severidad", "area_afectada", "descripcion", "entidades_relacionadas",
    "origen_alerta", "accion_recomendada", "requiere_revision_humana", "estado_alerta",
}

OBLIGATORIOS_DECISION = {
    "id_decision", "fecha_decision", "tipo_decision", "descripcion", "origen_decision", "area_responsable",
    "impacto_esperado", "nivel_riesgo", "requiere_revision_humana", "estado_decision",
}


def _tmp_local(nombre: str) -> Path:
    base = RUTA_BASE / "tests" / ".tmp"
    base.mkdir(parents=True, exist_ok=True)
    ruta = base / nombre
    if ruta.exists():
        shutil.rmtree(ruta)
    ruta.mkdir(parents=True, exist_ok=True)
    return ruta


def _contexto_fallback() -> dict:
    return cargar_contexto("x", "y", "z", "w", "k", "m", "n")


def test_estado_consolidado_y_reproducibilidad():
    ctx = _contexto_fallback()
    a = construir_estado_operativo(ctx, seed=42, dias=10)
    b = construir_estado_operativo(ctx, seed=42, dias=10)
    assert a == b
    assert "identidad_empresa" in a
    assert "metricas_operativas" in a


def test_estructura_completa_estado():
    ctx = _contexto_fallback()
    estado = construir_estado_operativo(ctx, seed=1, dias=7)
    assert "estado_por_areas" in estado
    assert "alertas_operativas" in estado
    assert "decisiones_simuladas" in estado
    assert "linea_tiempo_operativa" in estado


def test_metricas_indices_obligatorios():
    ctx = _contexto_fallback()
    estado = construir_estado_operativo(ctx, seed=2, dias=7)
    m = estado["metricas_operativas"]
    assert "indice_presion_operativa" in m
    assert "indice_riesgo_simulado" in m
    assert "indice_trazabilidad" in m


def test_alertas_campos_y_valores_controlados():
    ctx = _contexto_fallback()
    estado = construir_estado_operativo(ctx, seed=3, dias=7)
    alertas = estado["alertas_operativas"]
    assert OBLIGATORIOS_ALERTA.issubset(alertas[0].keys())
    assert all(a["severidad"] in SEVERIDADES for a in alertas)
    assert all(a["estado_alerta"] in ESTADOS_ALERTA for a in alertas)
    assert any(a["requiere_revision_humana"] for a in alertas)


def test_decisiones_campos_y_estado_controlado():
    ctx = _contexto_fallback()
    estado = construir_estado_operativo(ctx, seed=4, dias=7)
    decisiones = estado["decisiones_simuladas"]
    assert OBLIGATORIOS_DECISION.issubset(decisiones[0].keys())
    assert all(d["estado_decision"] in ESTADOS_DECISION for d in decisiones)


def test_areas_presion_y_consecuencias():
    ctx = _contexto_fallback()
    estado = construir_estado_operativo(ctx, seed=5, dias=7)
    areas = estado["estado_por_areas"]
    assert any(v["nivel_presion"] >= 1 for v in areas.values())
    consecuencias = generar_consecuencias_operativas(estado["alertas_operativas"], estado["decisiones_simuladas"])
    assert len(consecuencias) > 0


def test_exportaciones_completas():
    ctx = _contexto_fallback()
    estado = construir_estado_operativo(ctx, seed=6, dias=8)
    consecuencias = generar_consecuencias_operativas(estado["alertas_operativas"], estado["decisiones_simuladas"])
    resumen = construir_resumen_gemelo(estado, consecuencias, {"entrada": "fallback"})
    expediente = construir_expediente_estado_operativo(estado, consecuencias, resumen)
    salida = _tmp_local("out")
    rutas = exportar_gemelo_digital(estado, consecuencias, resumen, expediente, salida)

    assert Path(rutas["estado_operativo"]).exists()
    assert Path(rutas["metricas_json"]).exists()
    assert Path(rutas["metricas_csv"]).exists()
    assert Path(rutas["alertas_json"]).exists()
    assert Path(rutas["alertas_csv"]).exists()
    assert Path(rutas["decisiones_json"]).exists()
    assert Path(rutas["decisiones_csv"]).exists()
    assert Path(rutas["consecuencias_json"]).exists()
    assert Path(rutas["linea_tiempo_json"]).exists()
    assert Path(rutas["resumen_json"]).exists()
    assert Path(rutas["expediente_md"]).exists()


def test_sin_api_claves_datos_reales_sin_agentes_sin_monitorizacion_real():
    ctx = _contexto_fallback()
    estado = construir_estado_operativo(ctx, seed=7, dias=6)
    texto = json.dumps(estado, ensure_ascii=False).lower()
    assert "api_key" not in texto
    assert "token" not in texto
    assert "password" not in texto
    assert "ejecutar agentes reales" not in texto
    assert "monitorización real" not in texto
