"""Modelos de datos para escenarios de prueba."""

from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class EscenarioPrueba:
    id_escenario: str
    tipo_escenario: str
    titulo: str
    descripcion: str
    contexto_empresarial: str
    entrada_usuario_simulada: str
    objetivo_del_agente: str
    datos_disponibles: str
    restricciones: str
    riesgos_detectables: str
    comportamiento_esperado: str
    accion_recomendada: str
    requiere_revision_humana: bool
    nivel_dificultad: str
    criterio_evaluacion: str
    etiquetas: str
    origen_simulado: str


@dataclass
class ResumenEscenarios:
    total_escenarios: int
    escenarios_por_tipo: dict[str, int]
    escenarios_por_dificultad: dict[str, int]
    escenarios_que_requieren_revision_humana: int
    acciones_recomendadas: dict[str, int]
    entradas_utilizadas: dict[str, str]
    advertencia_sobre_datos_sinteticos: str
    advertencia_sobre_no_ejecucion_de_agentes: str


def dataclass_a_dict(objeto: Any) -> dict[str, Any]:
    return asdict(objeto)
