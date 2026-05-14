"""Modelos de datos del gemelo digital operativo ligero."""

from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class AlertaOperativa:
    id_alerta: str
    tipo_alerta: str
    severidad: str
    area_afectada: str
    descripcion: str
    entidades_relacionadas: str
    origen_alerta: str
    accion_recomendada: str
    requiere_revision_humana: bool
    estado_alerta: str


@dataclass
class DecisionSimulada:
    id_decision: str
    fecha_decision: str
    tipo_decision: str
    descripcion: str
    origen_decision: str
    area_responsable: str
    impacto_esperado: str
    nivel_riesgo: str
    requiere_revision_humana: bool
    estado_decision: str


@dataclass
class ConsecuenciaOperativa:
    id_consecuencia: str
    origen: str
    descripcion: str
    area_afectada: str
    impacto_estimado: str
    horizonte_temporal: str
    riesgo_residual: str
    accion_de_seguimiento: str


@dataclass
class HitoOperativo:
    fecha: str
    tipo_hito: str
    descripcion: str
    area_afectada: str
    severidad: str
    decision_relacionada: str
    requiere_revision_humana: bool


def dataclass_a_dict(objeto: Any) -> dict[str, Any]:
    return asdict(objeto)
