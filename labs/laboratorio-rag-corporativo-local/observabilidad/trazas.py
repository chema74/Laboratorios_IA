from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass
class Traza:
    nombre: str
    eventos: list[dict] = field(default_factory=list)

    def registrar(self, etapa: str, datos: dict) -> None:
        self.eventos.append(
            {
                "timestamp": datetime.now(UTC).isoformat(),
                "etapa": etapa,
                "datos": datos,
            }
        )


def crear_traza(nombre: str) -> Traza:
    return Traza(nombre=nombre)
