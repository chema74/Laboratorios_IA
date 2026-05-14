"""Construcción de línea temporal semanal para la demo narrativa."""

from __future__ import annotations

import random
from datetime import date, timedelta

from .modelos import HitoSemanal, dataclass_a_dict

SEVERIDADES = ["baja", "media", "alta", "critica"]


def construir_linea_tiempo(
    seed: int,
    dias: int,
    fecha_inicio: date,
    nombre_empresa: str,
    artefactos: dict[str, list[str]],
) -> list[dict]:
    rng = random.Random(seed)

    plantilla_hitos = [
        ("estado_inicial", "Inicio de semana operativa", "comercial"),
        ("evento_negocio", "Entrada de pedidos y pagos pendientes", "operaciones"),
        ("documentacion", "Generación de documentos de soporte", "soporte"),
        ("escenario_prueba", "Preparación de escenarios para evaluación", "direccion"),
        ("crisis_simulada", "Aparición de crisis operativa sintética", "operaciones"),
        ("revision_humana", "Activación de revisión humana simulada", "privacidad"),
        ("cierre_semanal", "Cierre técnico con comparativa de flujos", "direccion"),
    ]

    hitos: list[dict] = []
    for dia in range(1, dias + 1):
        tipo_hito, titulo_base, area = plantilla_hitos[(dia - 1) % len(plantilla_hitos)]
        severidad = rng.choices(SEVERIDADES, weights=[2, 3, 3, 2], k=1)[0]
        requiere_revision = severidad in {"alta", "critica"} or tipo_hito in {"crisis_simulada", "revision_humana"}
        artefactos_rel = artefactos.get(tipo_hito, [])
        decision = (
            "escalar_a_revision_humana"
            if requiere_revision
            else rng.choice(["continuar_monitoreo_simulado", "generar_resumen_operativo_simulado"])
        )

        hito = HitoSemanal(
            dia=dia,
            fecha_simulada=(fecha_inicio + timedelta(days=dia - 1)).isoformat(),
            tipo_hito=tipo_hito,
            titulo=f"{titulo_base} - {nombre_empresa}",
            descripcion=(
                "Hito sintético de la narrativa semanal. Se utiliza para explicar el "
                "funcionamiento del laboratorio sin representar actividad empresarial real."
            ),
            area_afectada=area,
            severidad=severidad,
            artefactos_relacionados=artefactos_rel,
            decision_simulada=decision,
            requiere_revision_humana=requiere_revision,
        )
        hitos.append(dataclass_a_dict(hito))

    return hitos

