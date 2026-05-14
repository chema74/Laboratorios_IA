"""Modelos de datos del comparador agente-proceso."""

from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class ProcesoComparado:
    id_proceso_comparado: str
    nombre_proceso: str
    descripcion: str
    contexto_utilizado: str
    criticidad: str
    requiere_revision_humana: bool
    riesgo_operativo_simulado: str
    origen_simulado: str


@dataclass
class ResultadoFlujo:
    id_resultado: str
    id_proceso_comparado: str
    tipo_flujo: str
    tiempo_estimado_minutos: float
    pasos_estimados: int
    errores_simulados: int
    nivel_trazabilidad: str
    nivel_consistencia: str
    carga_revision_humana: str
    riesgo_residual_simulado: str
    coste_relativo_simulado: float
    explicabilidad_operativa: str
    adecuacion_contexto: str
    limitaciones: str
    resultado_simulado: str


def dataclass_a_dict(objeto: Any) -> dict[str, Any]:
    return asdict(objeto)
