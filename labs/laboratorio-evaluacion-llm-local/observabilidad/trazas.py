from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class Traza:
    eventos: list[dict] = field(default_factory=list)

    def registrar(self, etapa: str, datos: dict) -> None:
        self.eventos.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "etapa": etapa,
            "datos": datos,
        })
