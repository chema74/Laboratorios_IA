"""Catálogo de procesos empresariales ficticios para comparación."""

from __future__ import annotations

from .modelos import ProcesoComparado, dataclass_a_dict

CRITICIDADES = ["baja", "media", "alta", "critica"]

BASE_PROCESOS = [
    ("revision_reclamacion_cliente", "Revisión de reclamación de cliente con evidencia disponible.", "alta", True),
    ("gestion_pago_pendiente", "Gestión operativa de pago pendiente con validación de estado.", "media", True),
    ("priorizacion_ticket_soporte", "Priorización de ticket de soporte según impacto y urgencia.", "media", False),
    ("revision_documento_sensible", "Revisión de documento sintético con sensibilidad ficticia.", "critica", True),
    ("respuesta_a_crisis_operativa", "Respuesta inicial a crisis sintética en curso.", "critica", True),
    ("analisis_alerta_privacidad", "Análisis de alerta sintética de privacidad y acceso.", "alta", True),
    ("resumen_estado_operativo", "Resumen sintético de estado operativo para seguimiento interno.", "baja", False),
]


def construir_procesos_comparados(contexto: dict, procesos: int = 7) -> list[dict]:
    salida: list[dict] = []
    total = max(1, min(procesos, len(BASE_PROCESOS)))
    for i in range(total):
        nombre, desc, crit, req = BASE_PROCESOS[i]
        p = ProcesoComparado(
            id_proceso_comparado=f"PRC-{i+1:05d}",
            nombre_proceso=nombre,
            descripcion=desc,
            contexto_utilizado="empresa,eventos,documentos,escenarios,crisis,revisiones,privacidad",
            criticidad=crit,
            requiere_revision_humana=req,
            riesgo_operativo_simulado="alto" if crit in {"alta", "critica"} else "medio",
            origen_simulado="comparador_agente_proceso_v1_local",
        )
        salida.append(dataclass_a_dict(p))
    return salida
