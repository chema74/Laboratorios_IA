"""Construcción del estado operativo consolidado del gemelo digital."""

from __future__ import annotations

import random
from datetime import date, timedelta

from .calculador_metricas import calcular_metricas_operativas, construir_identidad_empresa
from .modelos import DecisionSimulada, HitoOperativo, dataclass_a_dict
from .motor_alertas import SEVERIDADES, generar_alertas_operativas

ESTADOS_DECISION = ["propuesta", "pendiente_revision", "aceptada_simulada", "rechazada_simulada", "escalada"]


def _estado_areas(metricas: dict, alertas: list[dict], seed: int = 42) -> dict:
    azar = random.Random(seed + 200)
    areas = ["comercial", "operaciones", "soporte", "datos", "privacidad", "direccion"]
    salida: dict = {}

    for area in areas:
        alertas_area = [a for a in alertas if a["area_afectada"] == area]
        nivel_base = metricas["indice_presion_operativa"] / 20.0 + len(alertas_area)
        nivel_presion = int(max(1, min(10, round(nivel_base + azar.uniform(-1.0, 1.2), 0))))

        if nivel_presion <= 3:
            estado_area = "estable_simulado"
        elif nivel_presion <= 6:
            estado_area = "vigilancia_simulada"
        elif nivel_presion <= 8:
            estado_area = "tension_simulada"
        else:
            estado_area = "critico_simulado"

        salida[area] = {
            "estado_area": estado_area,
            "nivel_presion": nivel_presion,
            "alertas": len(alertas_area),
            "riesgos": "operativo,trazabilidad,continuidad",
            "acciones_recomendadas_simuladas": "revisar_datos,escalar_a_humano,generar_informe",
            "requiere_revision_humana": any(a["requiere_revision_humana"] for a in alertas_area),
        }

    return salida


def _generar_decisiones(alertas: list[dict], seed: int = 42) -> list[dict]:
    azar = random.Random(seed + 300)
    decisiones: list[dict] = []

    for i, alerta in enumerate(alertas, start=1):
        if alerta["requiere_revision_humana"]:
            estado = azar.choice(["pendiente_revision", "escalada", "propuesta"])
        else:
            estado = azar.choice(["propuesta", "aceptada_simulada", "rechazada_simulada"])

        decision = DecisionSimulada(
            id_decision=f"DEC-{i:05d}",
            fecha_decision=date.today().isoformat(),
            tipo_decision="gestion_alerta",
            descripcion=f"Decisión simulada para {alerta['id_alerta']} en área {alerta['area_afectada']}.",
            origen_decision="gemelo_digital_operativo_ligero",
            area_responsable=alerta["area_afectada"],
            impacto_esperado=azar.choice(["contener_riesgo", "mejorar_trazabilidad", "reducir_backlog"]),
            nivel_riesgo=alerta["severidad"],
            requiere_revision_humana=alerta["requiere_revision_humana"],
            estado_decision=estado,
        )
        decisiones.append(dataclass_a_dict(decision))

    return decisiones


def _generar_linea_tiempo(alertas: list[dict], decisiones: list[dict], dias: int, seed: int = 42) -> list[dict]:
    azar = random.Random(seed + 400)
    timeline: list[dict] = []
    base = date.today()

    for i in range(max(1, dias)):
        alerta = alertas[i % len(alertas)]
        decision = decisiones[i % len(decisiones)]
        hito = HitoOperativo(
            fecha=(base + timedelta(days=i)).isoformat(),
            tipo_hito=azar.choice(["alerta_detectada", "revision_programada", "decision_emitida", "seguimiento"]),
            descripcion=f"Hito operativo simulado asociado a {alerta['id_alerta']}.",
            area_afectada=alerta["area_afectada"],
            severidad=alerta["severidad"] if alerta["severidad"] in SEVERIDADES else "media",
            decision_relacionada=decision["id_decision"],
            requiere_revision_humana=decision["requiere_revision_humana"],
        )
        timeline.append(dataclass_a_dict(hito))

    return timeline


def construir_estado_operativo(contexto: dict, seed: int = 42, dias: int = 10) -> dict:
    """
    1) Calcula identidad y métricas operativas.
    2) Genera alertas, estado por áreas y decisiones simuladas.
    3) Construye línea temporal operativa para ventana de días.
    """
    identidad = construir_identidad_empresa(contexto)
    metricas = calcular_metricas_operativas(contexto)
    alertas = generar_alertas_operativas(contexto, metricas, seed=seed)
    metricas["alertas_activas"] = sum(1 for a in alertas if a["estado_alerta"] in {"activa", "en_revision"})
    areas = _estado_areas(metricas, alertas, seed=seed)
    decisiones = _generar_decisiones(alertas, seed=seed)
    linea_tiempo = _generar_linea_tiempo(alertas, decisiones, dias=dias, seed=seed)

    return {
        "identidad_empresa": identidad,
        "metricas_operativas": metricas,
        "estado_por_areas": areas,
        "alertas_operativas": alertas,
        "decisiones_simuladas": decisiones,
        "linea_tiempo_operativa": linea_tiempo,
    }
