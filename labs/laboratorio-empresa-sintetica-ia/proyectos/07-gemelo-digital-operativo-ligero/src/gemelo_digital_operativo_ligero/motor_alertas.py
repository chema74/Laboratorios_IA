"""Generación de alertas operativas sintéticas."""

from __future__ import annotations

import random

from .modelos import AlertaOperativa, dataclass_a_dict

SEVERIDADES = ["baja", "media", "alta", "critica"]
ESTADOS_ALERTA = ["activa", "en_revision", "mitigada_simulada", "cerrada_simulada"]


def generar_alertas_operativas(contexto: dict, metricas: dict, seed: int = 42) -> list[dict]:
    """
    1) Construye alertas desde métricas y crisis.
    2) Mantiene severidad y estado en catálogos controlados.
    """
    azar = random.Random(seed + 100)
    alertas: list[dict] = []

    reglas = [
        ("pagos_pendientes_altos", metricas["pagos_pendientes"] > 8, "finanzas", "Pagos pendientes por encima del umbral sintético."),
        ("incidencias_activas_altas", metricas["incidencias_activas"] > 6, "operaciones", "Incidencias activas acumuladas en operación."),
        ("presion_operativa", metricas["indice_presion_operativa"] > 60, "direccion", "Índice de presión operativa en rango elevado."),
        ("riesgo_privacidad", any(c.get("tipo_crisis") == "incidente_privacidad" for c in contexto.get("crisis", [])), "privacidad", "Riesgo sintético de privacidad detectado en crisis."),
    ]

    idx = 1
    for tipo, condicion, area, descripcion in reglas:
        if condicion:
            severidad = azar.choice(SEVERIDADES[1:])
            estado = "activa" if severidad in {"alta", "critica"} else azar.choice(ESTADOS_ALERTA)
            alerta = AlertaOperativa(
                id_alerta=f"ALT-{idx:05d}",
                tipo_alerta=tipo,
                severidad=severidad,
                area_afectada=area,
                descripcion=descripcion,
                entidades_relacionadas="clientes,procesos",
                origen_alerta="reglas_metricas_y_crisis_sinteticas",
                accion_recomendada=azar.choice(["escalar_a_humano", "revisar_datos", "generar_informe", "auditar_eventos"]),
                requiere_revision_humana=severidad in {"alta", "critica"},
                estado_alerta=estado,
            )
            alertas.append(dataclass_a_dict(alerta))
            idx += 1

    if not alertas:
        alerta = AlertaOperativa(
            id_alerta="ALT-00001",
            tipo_alerta="seguimiento_operativo",
            severidad="media",
            area_afectada="operaciones",
            descripcion="Seguimiento sintético preventivo sin incidentes críticos.",
            entidades_relacionadas="procesos",
            origen_alerta="fallback_alerta_sintetica",
            accion_recomendada="generar_informe",
            requiere_revision_humana=False,
            estado_alerta="en_revision",
        )
        alertas.append(dataclass_a_dict(alerta))

    return alertas
