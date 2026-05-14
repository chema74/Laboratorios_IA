from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class Traza:
    nombre: str
    eventos: list[dict] = field(default_factory=list)

    def registrar(self, etapa: str, datos: dict) -> None:
        self.eventos.append(
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "etapa": etapa,
                "datos": datos,
            }
        )


def crear_traza(nombre: str) -> Traza:
    return Traza(nombre=nombre)
