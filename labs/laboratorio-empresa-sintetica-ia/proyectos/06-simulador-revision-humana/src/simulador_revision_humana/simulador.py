"""Simulador determinista de revisiones humanas ficticias."""

from __future__ import annotations

import random
from datetime import date, timedelta

from .catalogo_criterios import (
    CRITERIOS_BASE,
    DECISIONES_CONTROLADAS,
    MAPEO_ACCION_POR_DECISION,
    NIVELES_CONFIANZA,
    ROLES_REVISORES,
)
from .modelos import RevisionHumana, dataclass_a_dict


def _pool_elementos(contexto: dict) -> list[dict]:
    pool: list[dict] = []
    for e in contexto.get("eventos", []):
        pool.append(
            {
                "tipo_elemento_revisado": "evento_negocio",
                "id_elemento_revisado": e.get("id_evento", "EVT-000001"),
                "titulo_elemento": e.get("tipo_evento", "evento_negocio"),
            }
        )
    for d in contexto.get("documentos", []):
        pool.append(
            {
                "tipo_elemento_revisado": "documento_sintetico",
                "id_elemento_revisado": d.get("id_documento", "DOC-000001"),
                "titulo_elemento": d.get("tipo_documento", d.get("titulo", "documento_sintetico")),
            }
        )
    for s in contexto.get("escenarios", []):
        pool.append(
            {
                "tipo_elemento_revisado": "escenario_prueba_agente",
                "id_elemento_revisado": s.get("id_escenario", "ESC-000001"),
                "titulo_elemento": s.get("tipo_escenario", "escenario_prueba_agente"),
            }
        )
    for c in contexto.get("crisis", []):
        pool.append(
            {
                "tipo_elemento_revisado": "crisis_simulada",
                "id_elemento_revisado": c.get("id_crisis", "CRS-00001"),
                "titulo_elemento": c.get("tipo_crisis", "crisis_simulada"),
            }
        )

    if not pool:
        pool.append(
            {
                "tipo_elemento_revisado": "evento_negocio",
                "id_elemento_revisado": "EVT-000001",
                "titulo_elemento": "evento_negocio",
            }
        )
    return pool


def simular_revisiones_humanas(
    contexto: dict,
    seed: int = 42,
    revisiones: int = 20,
    porcentaje_escalado: int = 25,
) -> list[dict]:
    """
    1) Construye un pool de elementos revisables.
    2) Genera decisiones controladas con semilla reproducible.
    3) Devuelve revisiones con trazabilidad explícita.
    """
    azar = random.Random(seed)
    pool = _pool_elementos(contexto)
    fecha_base = date.today()

    revisiones_generadas: list[dict] = []

    for i in range(1, revisiones + 1):
        elemento = pool[(i - 1) % len(pool)]

        # Paso 1: controlar tasa de escalado según parámetro.
        if azar.random() < max(0, min(100, porcentaje_escalado)) / 100.0:
            decision = "escalar"
        else:
            decision = azar.choice([d for d in DECISIONES_CONTROLADAS if d != "escalar"])

        accion = MAPEO_ACCION_POR_DECISION[decision]
        nivel_confianza = azar.choice(NIVELES_CONFIANZA)
        rol = azar.choice(ROLES_REVISORES)
        criterios = ",".join(sorted(azar.sample(CRITERIOS_BASE, k=2)))
        requiere_segunda = decision in {"escalar", "bloquear_accion", "registrar_incidente"} or nivel_confianza == "baja"

        revision = RevisionHumana(
            id_revision=f"REV-{i:06d}",
            tipo_elemento_revisado=elemento["tipo_elemento_revisado"],
            id_elemento_revisado=elemento["id_elemento_revisado"],
            titulo_elemento=f"Revisión de {elemento['titulo_elemento']}",
            fecha_revision=(fecha_base + timedelta(days=i % 10)).isoformat(),
            revisor_ficticio=f"Revisor Ficticio {((i - 1) % 7) + 1}",
            rol_revisor=rol,
            decision=decision,
            motivo_decision="Resultado simulado en función de criterios de revisión ficticia.",
            nivel_confianza_humana=nivel_confianza,
            criterios_aplicados=criterios,
            cambios_sugeridos="Ajustar trazabilidad, validar datos sintéticos y registrar justificación.",
            accion_posterior=accion,
            requiere_segunda_revision=requiere_segunda,
            trazabilidad=f"origen={elemento['tipo_elemento_revisado']}|id={elemento['id_elemento_revisado']}|revision=REV-{i:06d}",
            origen_simulado="simulador_revision_humana_v1_local",
        )
        revisiones_generadas.append(dataclass_a_dict(revision))

    return revisiones_generadas
