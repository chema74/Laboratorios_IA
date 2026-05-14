from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

RUTA_BASE = Path(__file__).resolve().parents[1]
RUTA_SRC = RUTA_BASE / "src"
if str(RUTA_SRC) not in sys.path:
    sys.path.insert(0, str(RUTA_SRC))

from comparador_agente_proceso.cargador_contexto import cargar_contexto
from comparador_agente_proceso.catalogo_procesos import CRITICIDADES, construir_procesos_comparados
from comparador_agente_proceso.comparador import RECOMENDADOS, construir_comparaciones
from comparador_agente_proceso.evaluador_metricas import construir_expediente, construir_resumen
from comparador_agente_proceso.exportador import exportar_resultados
from comparador_agente_proceso.simulador_flujos import (
    CARGA_REVISION,
    CONSISTENCIA,
    RESULTADO_SIMULADO,
    RIESGO_RESIDUAL,
    TIPOS_FLUJO,
    TRAZABILIDAD,
    simular_resultados_flujos,
)

OBLIG_PROCESO = {
    "id_proceso_comparado", "nombre_proceso", "descripcion", "contexto_utilizado", "criticidad",
    "requiere_revision_humana", "riesgo_operativo_simulado", "origen_simulado",
}

OBLIG_RESULTADO = {
    "id_resultado", "id_proceso_comparado", "tipo_flujo", "tiempo_estimado_minutos", "pasos_estimados",
    "errores_simulados", "nivel_trazabilidad", "nivel_consistencia", "carga_revision_humana",
    "riesgo_residual_simulado", "coste_relativo_simulado", "explicabilidad_operativa", "adecuacion_contexto",
    "limitaciones", "resultado_simulado",
}


def _tmp(nombre: str) -> Path:
    base = RUTA_BASE / "tests" / ".tmp"
    base.mkdir(parents=True, exist_ok=True)
    p = base / nombre
    if p.exists():
        shutil.rmtree(p)
    p.mkdir(parents=True, exist_ok=True)
    return p


def _ctx() -> dict:
    paths = {
        "entrada_empresa": "x", "entrada_eventos": "y", "entrada_documentos": "z", "entrada_escenarios": "w",
        "entrada_crisis": "k", "entrada_revisiones": "m", "entrada_registro_decisiones": "n",
        "entrada_estado_operativo": "o", "entrada_alertas": "p", "entrada_decisiones": "q",
        "entrada_inventario_privacidad": "r", "entrada_riesgos_privacidad": "s",
    }
    return cargar_contexto(paths)


def test_procesos_y_reproducibilidad():
    ctx = _ctx()
    p1 = construir_procesos_comparados(ctx, procesos=7)
    p2 = construir_procesos_comparados(ctx, procesos=7)
    assert p1 == p2
    assert len(p1) == 7


def test_procesos_campos_y_criticidad_controlada():
    p = construir_procesos_comparados(_ctx(), procesos=7)
    assert OBLIG_PROCESO.issubset(p[0].keys())
    assert all(x["criticidad"] in CRITICIDADES for x in p)


def test_tres_flujos_y_campos_resultado():
    p = construir_procesos_comparados(_ctx(), procesos=4)
    r = simular_resultados_flujos(p, seed=42)
    tipos = {x["tipo_flujo"] for x in r}
    assert set(TIPOS_FLUJO) == tipos
    assert OBLIG_RESULTADO.issubset(r[0].keys())


def test_valores_controlados_resultados():
    p = construir_procesos_comparados(_ctx(), procesos=7)
    r = simular_resultados_flujos(p, seed=7)
    assert all(x["tipo_flujo"] in TIPOS_FLUJO for x in r)
    assert all(x["nivel_trazabilidad"] in TRAZABILIDAD for x in r)
    assert all(x["nivel_consistencia"] in CONSISTENCIA for x in r)
    assert all(x["carga_revision_humana"] in CARGA_REVISION for x in r)
    assert all(x["riesgo_residual_simulado"] in RIESGO_RESIDUAL for x in r)
    assert all(x["resultado_simulado"] in RESULTADO_SIMULADO for x in r)


def test_comparaciones_y_recomendaciones_controladas():
    p = construir_procesos_comparados(_ctx(), procesos=7)
    r = simular_resultados_flujos(p, seed=9)
    c = construir_comparaciones(p, r)
    assert len(c) == len(p)
    assert all(x["flujo_recomendado_simulado"] in RECOMENDADOS for x in c)
    assert any(x["flujo_recomendado_simulado"] in {"hibrido_con_revision_humana", "no_recomendado_automatizar"} for x in c)


def test_exportaciones_completas():
    p = construir_procesos_comparados(_ctx(), procesos=7)
    r = simular_resultados_flujos(p, seed=11)
    c = construir_comparaciones(p, r)
    resumen = construir_resumen(p, r, c, {"entrada": "fallback"})
    expediente = construir_expediente(p, r, c, resumen)
    rutas = exportar_resultados(p, r, c, resumen, expediente, _tmp("out"))

    for k in ["procesos_json", "procesos_csv", "resultados_json", "resultados_csv", "comparaciones_json", "comparaciones_csv", "resumen_json", "expediente_md"]:
        assert Path(rutas[k]).exists()


def test_sin_api_claves_datos_reales_sin_agentes_sin_benchmark_real_sin_recomendacion_real():
    p = construir_procesos_comparados(_ctx(), procesos=3)
    r = simular_resultados_flujos(p, seed=13)
    c = construir_comparaciones(p, r)
    texto = json.dumps({"p": p, "r": r, "c": c}, ensure_ascii=False).lower()
    assert "api_key" not in texto
    assert "token" not in texto
    assert "password" not in texto
    assert "agente_real_ejecutado" not in texto
    assert "benchmark real" not in texto
    assert "recomendacion_empresarial_real_aprobada" not in texto


