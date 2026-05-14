from dataclasses import dataclass


@dataclass
class RespuestaAPI:
    estado: str
    codigo_interno: str
    mensaje: str
    datos: dict
    trazabilidad: dict
