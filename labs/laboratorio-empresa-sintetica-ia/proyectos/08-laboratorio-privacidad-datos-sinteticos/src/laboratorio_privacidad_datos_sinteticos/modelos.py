"""Modelos de datos del laboratorio de privacidad sintética."""

from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class InventarioDato:
    id_dato: str
    origen: str
    tipo_entidad: str
    campo: str
    valor_simulado_resumido: str
    nivel_sensibilidad_ficticia: str
    categoria_privacidad_simulada: str
    uso_previsto: str
    requiere_minimizacion: bool
    requiere_anonimizacion: bool
    requiere_revision_humana: bool
    origen_simulado: str


@dataclass
class RiesgoPrivacidad:
    id_riesgo: str
    tipo_riesgo: str
    descripcion: str
    origen: str
    severidad: str
    datos_afectados: str
    rol_afectado: str
    recomendacion_simulada: str
    requiere_revision_humana: bool
    estado_riesgo: str


def dataclass_a_dict(objeto: Any) -> dict[str, Any]:
    return asdict(objeto)
