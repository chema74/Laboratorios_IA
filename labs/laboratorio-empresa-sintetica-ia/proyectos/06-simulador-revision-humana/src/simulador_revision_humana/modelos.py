"""Modelos de datos para revisión humana simulada."""

from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class RevisionHumana:
    id_revision: str
    tipo_elemento_revisado: str
    id_elemento_revisado: str
    titulo_elemento: str
    fecha_revision: str
    revisor_ficticio: str
    rol_revisor: str
    decision: str
    motivo_decision: str
    nivel_confianza_humana: str
    criterios_aplicados: str
    cambios_sugeridos: str
    accion_posterior: str
    requiere_segunda_revision: bool
    trazabilidad: str
    origen_simulado: str


@dataclass
class RegistroDecision:
    id_registro: str
    id_revision: str
    fecha_registro: str
    decision: str
    accion_posterior: str
    resumen_trazabilidad: str
    impacto_simulado: str
    estado_registro: str


def dataclass_a_dict(objeto: Any) -> dict[str, Any]:
    return asdict(objeto)
