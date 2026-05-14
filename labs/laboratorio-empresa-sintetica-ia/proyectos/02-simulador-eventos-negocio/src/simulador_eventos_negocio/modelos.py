"""Modelos de datos para simulación de eventos."""

from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class EventoNegocio:
    id_evento: str
    tipo_evento: str
    fecha_evento: str
    severidad: str
    entidad_afectada: str
    id_entidad_afectada: str
    descripcion: str
    estado_evento: str
    origen_simulado: str
    requiere_revision_humana: bool
    impacto_estimado: float


@dataclass
class ResumenEventos:
    total_eventos: int
    eventos_por_tipo: dict[str, int]
    eventos_por_severidad: dict[str, int]
    eventos_que_requieren_revision_humana: int
    alertas_operativas: int
    fecha_inicio_simulacion: str
    fecha_fin_simulacion: str


def dataclass_a_dict(objeto: Any) -> dict[str, Any]:
    return asdict(objeto)
