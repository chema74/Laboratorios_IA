"""Generación de registro agregado y resumen de revisión humana."""

from __future__ import annotations

import random
from collections import Counter
from datetime import date

from .catalogo_criterios import ESTADOS_REGISTRO
from .modelos import RegistroDecision, dataclass_a_dict


def generar_registro_decisiones(revisiones: list[dict], seed: int = 42) -> list[dict]:
    azar = random.Random(seed + 500)
    registros: list[dict] = []

    for i, rev in enumerate(revisiones, start=1):
        if rev["decision"] == "escalar":
            estado = "escalado"
        elif rev["requiere_segunda_revision"]:
            estado = "pendiente"
        else:
            estado = azar.choice([e for e in ESTADOS_REGISTRO if e != "escalado"])

        reg = RegistroDecision(
            id_registro=f"REG-{i:06d}",
            id_revision=rev["id_revision"],
            fecha_registro=date.today().isoformat(),
            decision=rev["decision"],
            accion_posterior=rev["accion_posterior"],
            resumen_trazabilidad=f"Registro derivado de {rev['trazabilidad']}",
            impacto_simulado=azar.choice(["bajo", "medio", "alto"]),
            estado_registro=estado,
        )
        registros.append(dataclass_a_dict(reg))

    return registros


def construir_resumen_revision_humana(revisiones: list[dict], registros: list[dict], entradas_utilizadas: dict[str, str]) -> dict:
    por_tipo = Counter(x["tipo_elemento_revisado"] for x in revisiones)
    por_decision = Counter(x["decision"] for x in revisiones)
    por_accion = Counter(x["accion_posterior"] for x in revisiones)
    por_rol = Counter(x["rol_revisor"] for x in revisiones)
    por_confianza = Counter(x["nivel_confianza_humana"] for x in revisiones)
    segunda = sum(1 for x in revisiones if x.get("requiere_segunda_revision"))

    return {
        "total_revisiones": len(revisiones),
        "revisiones_por_tipo_elemento": dict(por_tipo),
        "decisiones_por_tipo": dict(por_decision),
        "acciones_posteriores": dict(por_accion),
        "revisiones_que_requieren_segunda_revision": segunda,
        "roles_revisores": dict(por_rol),
        "nivel_confianza_humana": dict(por_confianza),
        "entradas_utilizadas": entradas_utilizadas,
        "advertencia_sobre_revision_simulada": "Este resultado corresponde a una revisión sintética, no humana real.",
        "advertencia_sobre_no_validacion_profesional_real": "No constituye validación profesional real ni cumplimiento operativo real.",
        "total_registros_decision": len(registros),
    }


def construir_expediente_revision_markdown(revisiones: list[dict], resumen: dict) -> str:
    filas = "\n".join(
        [f"- {r['id_revision']} | {r['tipo_elemento_revisado']} | decision={r['decision']} | accion={r['accion_posterior']}" for r in revisiones[:20]]
    )

    escalados = [r for r in revisiones if r["decision"] == "escalar"]
    criterios = sorted({c for r in revisiones for c in r["criterios_aplicados"].split(",") if c})

    return (
        "# Expediente de Revisión Humana Simulada\n\n"
        "**Aviso:** Simulación sintética para pruebas internas. No representa revisión humana real.\n\n"
        "## Resumen ejecutivo ficticio\n"
        f"Se generaron {resumen['total_revisiones']} revisiones y {resumen['total_registros_decision']} registros de decisión.\n\n"
        "## Revisiones simuladas\n"
        f"{filas}\n\n"
        "## Decisiones agregadas\n"
        f"{resumen['decisiones_por_tipo']}\n\n"
        "## Casos escalados\n"
        f"Total escalados: {len(escalados)}\n\n"
        "## Revisiones con segunda revisión\n"
        f"Total: {resumen['revisiones_que_requieren_segunda_revision']}\n\n"
        "## Criterios aplicados\n"
        f"{', '.join(criterios)}\n\n"
        "## Límites de uso\n"
        "- No usar como validación profesional real.\n"
        "- No usar para cumplimiento real.\n"
        "- No usar para decisiones operativas reales.\n\n"
        "## Nota final\n"
        "No existe validación profesional real ni revisión humana real en este expediente.\n"
    )
