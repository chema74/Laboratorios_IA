from dataclasses import dataclass


@dataclass
class CasoUsoIA:
    identificador: str
    nombre: str
    area: str
    criticidad: str
    grado_automatizacion: str
