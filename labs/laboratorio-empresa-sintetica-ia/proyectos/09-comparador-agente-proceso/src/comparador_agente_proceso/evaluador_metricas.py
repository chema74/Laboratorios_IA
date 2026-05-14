"""Resumen de métricas agregadas del comparador."""

from __future__ import annotations

from collections import Counter, defaultdict
from datetime import date


def construir_resumen(procesos: list[dict], resultados: list[dict], comparaciones: list[dict], entradas: dict[str, str]) -> dict:
    por_flujo_tiempo: dict[str, list[float]] = defaultdict(list)
    por_flujo_errores = Counter()
    por_flujo_traz = Counter()
    por_flujo_consistencia = Counter()
    por_flujo_carga = Counter()
    por_flujo_riesgo = Counter()

    for r in resultados:
        f = r["tipo_flujo"]
        por_flujo_tiempo[f].append(float(r["tiempo_estimado_minutos"]))
        por_flujo_errores[f] += int(r["errores_simulados"])
        por_flujo_traz[f + "::" + r["nivel_trazabilidad"]] += 1
        por_flujo_consistencia[f + "::" + r["nivel_consistencia"]] += 1
        por_flujo_carga[f + "::" + r["carga_revision_humana"]] += 1
        por_flujo_riesgo[f + "::" + r["riesgo_residual_simulado"]] += 1

    promedio_tiempo = {
        f: round(sum(v) / len(v), 2) if v else 0.0
        for f, v in por_flujo_tiempo.items()
    }

    recomendaciones = Counter(c["flujo_recomendado_simulado"] for c in comparaciones)

    return {
        "fecha_generacion": date.today().isoformat(),
        "total_procesos_comparados": len(procesos),
        "flujos_evaluados": ["manual", "automatizado_clasico", "asistido_por_agente"],
        "promedio_tiempo_por_flujo": promedio_tiempo,
        "errores_simulados_por_flujo": dict(por_flujo_errores),
        "trazabilidad_por_flujo": dict(por_flujo_traz),
        "consistencia_por_flujo": dict(por_flujo_consistencia),
        "carga_revision_humana_por_flujo": dict(por_flujo_carga),
        "riesgo_residual_por_flujo": dict(por_flujo_riesgo),
        "recomendaciones_por_tipo": dict(recomendaciones),
        "entradas_utilizadas": entradas,
        "advertencia_sobre_datos_sinteticos": "Resultados sintéticos sobre datos ficticios.",
        "advertencia_sobre_no_benchmark_real": "No usar como benchmark real ni como medición empresarial real.",
        "advertencia_sobre_no_ejecucion_de_agentes": "No se ejecutan agentes reales; flujo asistido es simulado.",
    }


def construir_expediente(procesos: list[dict], resultados: list[dict], comparaciones: list[dict], resumen: dict) -> str:
    p_txt = "\n".join([f"- {p['id_proceso_comparado']} | {p['nombre_proceso']} | criticidad={p['criticidad']}" for p in procesos])
    r_txt = "\n".join([f"- {r['id_resultado']} | {r['id_proceso_comparado']} | {r['tipo_flujo']} | tiempo={r['tiempo_estimado_minutos']}" for r in resultados[:25]])
    c_txt = "\n".join([f"- {c['id_comparacion']} | {c['proceso']} | recomendado={c['flujo_recomendado_simulado']}" for c in comparaciones])

    return (
        "# Expediente Comparador Agente-Proceso\n\n"
        "**Aviso:** Simulación sintética para portfolio. No es benchmark real.\n\n"
        "## Resumen ejecutivo ficticio\n"
        f"Se compararon {resumen['total_procesos_comparados']} procesos en tres flujos simulados.\n\n"
        "## Procesos comparados\n"
        f"{p_txt}\n\n"
        "## Resultados por flujo\n"
        f"{r_txt}\n\n"
        "## Comparación manual vs automatizado clásico vs agente simulado\n"
        f"{c_txt}\n\n"
        "## Recomendaciones simuladas\n"
        "Los resultados son orientativos y simulados; requieren validación humana previa.\n\n"
        "## Limitaciones\n"
        "- No benchmark real.\n"
        "- No evaluación productiva real.\n"
        "- No ejecución real de agentes.\n\n"
        "## Nota final\n"
        "No existe recomendación empresarial real ni consultoría real en este comparador.\n"
    )
