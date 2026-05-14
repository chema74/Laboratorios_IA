from dataclasses import dataclass


@dataclass
class ResultadoCaso:
    caso_id: str
    respuesta_id: str
    puntuacion_total: float
    detalle: dict
