from dataclasses import dataclass


@dataclass
class DeteccionPII:
    tipo: str
    valor: str
    inicio: int
    severidad: str
