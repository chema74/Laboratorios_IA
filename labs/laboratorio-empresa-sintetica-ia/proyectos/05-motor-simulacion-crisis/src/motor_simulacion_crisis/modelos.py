"""Modelos de datos para crisis simuladas."""

from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class CrisisSimulada:
    id_crisis: str
    tipo_crisis: str
    titulo: str
    descripcion: str
    fecha_inicio: str
    fecha_fin_estimada: str
    severidad: str
    areas_afectadas: str
    entidades_afectadas: str
    eventos_relacionados: str
    documentos_relacionados: str
    escenarios_relacionados: str
    indicadores_impacto: str
    senales_tempranas: str
    decisiones_recomendadas: str
    riesgos_secundarios: str
    requiere_revision_humana: bool
    estado_crisis: str
    origen_simulado: str


@dataclass
class HitoLineaTiempo:
    fecha: str
    id_crisis: str
    tipo_hito: str
    descripcion: str
    impacto_estimado: float
    decision_pendiente: str
    requiere_revision_humana: bool


def dataclass_a_dict(objeto: Any) -> dict[str, Any]:
    return asdict(objeto)
