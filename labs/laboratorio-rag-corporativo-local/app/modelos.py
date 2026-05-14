from dataclasses import dataclass, field
from typing import Any


@dataclass
class Fragmento:
    fragmento_id: str
    doc_id: str
    titulo: str
    area: str
    etiquetas: list[str]
    contenido: str


@dataclass
class ResultadoRecuperacion:
    fragmento: Fragmento
    puntuacion: float
    detalle: dict[str, Any] = field(default_factory=dict)
