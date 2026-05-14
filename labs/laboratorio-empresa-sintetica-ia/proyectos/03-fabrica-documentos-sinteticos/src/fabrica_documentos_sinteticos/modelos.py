"""Modelos de datos para documentos sintéticos."""

from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class DocumentoSintetico:
    id_documento: str
    tipo_documento: str
    titulo: str
    fecha_documento: str
    entidad_relacionada: str
    id_entidad_relacionada: str
    origen_simulado: str
    nivel_sensibilidad_ficticia: str
    requiere_revision_humana: bool
    ruta_markdown: str
    estado_documento: str
    contenido_markdown: str


@dataclass
class ResumenDocumentos:
    total_documentos: int
    documentos_por_tipo: dict[str, int]
    documentos_que_requieren_revision_humana: int
    niveles_sensibilidad_ficticia: dict[str, int]
    fecha_generacion: str
    entradas_utilizadas: dict[str, str]
    advertencia_sobre_datos_sinteticos: str


def dataclass_a_dict(objeto: Any) -> dict[str, Any]:
    return asdict(objeto)
