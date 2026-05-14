"""Simulación de resultados de flujos manual/automatizado/agente simulado."""

from __future__ import annotations

import random

from .modelos import ResultadoFlujo, dataclass_a_dict

TIPOS_FLUJO = ["manual", "automatizado_clasico", "asistido_por_agente"]
TRAZABILIDAD = ["baja", "media", "alta"]
CONSISTENCIA = ["baja", "media", "alta"]
CARGA_REVISION = ["baja", "media", "alta"]
RIESGO_RESIDUAL = ["bajo", "medio", "alto", "critico"]
RESULTADO_SIMULADO = ["correcto_simulado", "incompleto_simulado", "requiere_revision", "bloqueado_por_riesgo", "escalado"]


def simular_resultados_flujos(procesos: list[dict], seed: int = 42) -> list[dict]:
    """
    1) Genera tres flujos por proceso.
    2) Ajusta valores por tipo de flujo y criticidad.
    3) Mantiene métricas y estados en catálogos controlados.
    """
    azar = random.Random(seed)
    resultados: list[dict] = []
    idx = 1

    for p in procesos:
        crit = p["criticidad"]
        for flujo in TIPOS_FLUJO:
            base_tiempo = {"manual": 45, "automatizado_clasico": 25, "asistido_por_agente": 18}[flujo]
            factor_crit = {"baja": 0.8, "media": 1.0, "alta": 1.25, "critica": 1.6}[crit]
            tiempo = round(base_tiempo * factor_crit + azar.uniform(-3.0, 4.0), 2)

            base_errores = {"manual": 3, "automatizado_clasico": 2, "asistido_por_agente": 2}[flujo]
            if crit in {"alta", "critica"}:
                base_errores += 1
            errores = max(0, base_errores + azar.randrange(-1, 2))

            traz = {"manual": "media", "automatizado_clasico": "alta", "asistido_por_agente": "alta"}[flujo]
            consist = {"manual": "media", "automatizado_clasico": "alta", "asistido_por_agente": "media"}[flujo]
            carga = {"manual": "alta", "automatizado_clasico": "media", "asistido_por_agente": "media"}[flujo]
            riesgo = {"manual": "medio", "automatizado_clasico": "medio", "asistido_por_agente": "alto"}[flujo]

            if crit == "critica" and flujo == "asistido_por_agente":
                resultado = "bloqueado_por_riesgo"
            elif p["requiere_revision_humana"] and flujo == "asistido_por_agente":
                resultado = "requiere_revision"
            else:
                resultado = azar.choice(["correcto_simulado", "incompleto_simulado", "escalado"])

            r = ResultadoFlujo(
                id_resultado=f"RES-{idx:06d}",
                id_proceso_comparado=p["id_proceso_comparado"],
                tipo_flujo=flujo,
                tiempo_estimado_minutos=max(1.0, tiempo),
                pasos_estimados=max(2, int(tiempo // 4)),
                errores_simulados=errores,
                nivel_trazabilidad=traz,
                nivel_consistencia=consist,
                carga_revision_humana=carga,
                riesgo_residual_simulado=riesgo,
                coste_relativo_simulado=round({"manual": 1.0, "automatizado_clasico": 0.8, "asistido_por_agente": 0.7}[flujo] * factor_crit, 2),
                explicabilidad_operativa=azar.choice(["alta", "media"]),
                adecuacion_contexto=azar.choice(["alta", "media", "baja"]),
                limitaciones="Resultado sintético sin ejecución real de agentes.",
                resultado_simulado=resultado,
            )
            resultados.append(dataclass_a_dict(r))
            idx += 1

    return resultados
