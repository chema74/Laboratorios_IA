"""Construcción de comparaciones por proceso y recomendación simulada."""

from __future__ import annotations

RECOMENDADOS = ["manual", "automatizado_clasico", "asistido_por_agente", "hibrido_con_revision_humana", "no_recomendado_automatizar"]


def construir_comparaciones(procesos: list[dict], resultados: list[dict]) -> list[dict]:
    comparaciones: list[dict] = []

    for i, p in enumerate(procesos, start=1):
        subset = [r for r in resultados if r["id_proceso_comparado"] == p["id_proceso_comparado"]]
        by_flujo = {r["tipo_flujo"]: r for r in subset}

        if p["criticidad"] == "critica":
            recomendado = "no_recomendado_automatizar"
            motivo = "Proceso crítico con riesgo operativo elevado: mantener control humano reforzado."
        elif p["requiere_revision_humana"]:
            recomendado = "hibrido_con_revision_humana"
            motivo = "Requiere validación humana para reducir riesgo residual simulado."
        else:
            candidatos = sorted(subset, key=lambda x: (x["errores_simulados"], x["tiempo_estimado_minutos"]))
            recomendado = candidatos[0]["tipo_flujo"] if candidatos else "manual"
            motivo = "Selección por menor error simulado y tiempo estimado en contexto sintético."

        comparaciones.append(
            {
                "id_comparacion": f"CMP-{i:05d}",
                "proceso": p["nombre_proceso"],
                "flujos_comparados": "manual|automatizado_clasico|asistido_por_agente",
                "flujo_recomendado_simulado": recomendado,
                "motivo_recomendacion": motivo,
                "advertencias": "Resultado sintético. No usar como benchmark ni recomendación empresarial real.",
                "no_usar_como_benchmark_real": True,
                "requiere_validacion_humana": recomendado in {"hibrido_con_revision_humana", "no_recomendado_automatizar"},
                "resumen_flujos": {
                    "manual": by_flujo.get("manual", {}),
                    "automatizado_clasico": by_flujo.get("automatizado_clasico", {}),
                    "asistido_por_agente": by_flujo.get("asistido_por_agente", {}),
                },
            }
        )

    return comparaciones
