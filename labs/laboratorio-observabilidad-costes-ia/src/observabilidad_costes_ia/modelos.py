from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class EventoObservabilidad:
    id_evento: str
    caso_uso: str
    modelo: str
    proveedor: str
    tokens_entrada: int
    tokens_salida: int
    latencia_ms: int
    coste_estimado_eur: float
    estado: str
    riesgo: str
    equipo: str
    usuario: str
    timestamp: str
    trazabilidad: str


CAMPOS_REQUERIDOS = {
    "id_evento",
    "caso_uso",
    "modelo",
    "proveedor",
    "tokens_entrada",
    "tokens_salida",
    "latencia_ms",
    "coste_estimado_eur",
    "estado",
    "riesgo",
    "equipo",
    "usuario",
    "timestamp",
    "trazabilidad",
}


def normalizar_evento(evento: dict[str, Any], indice: int) -> dict[str, Any]:
    limpio = dict(evento)
    limpio.setdefault("id_evento", f"EV-{indice:04d}")
    limpio.setdefault("estado", "ok")
    limpio.setdefault("riesgo", "bajo")
    limpio.setdefault("equipo", "equipo_general")
    limpio.setdefault("usuario", "usuario_demo")
    limpio.setdefault("modelo", "modelo_local")
    limpio.setdefault("proveedor", "local")
    limpio.setdefault("trazabilidad", f"traza-{limpio['id_evento']}")
    limpio.setdefault("timestamp", datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"))

    limpio["tokens_entrada"] = int(limpio.get("tokens_entrada", 0))
    limpio["tokens_salida"] = int(limpio.get("tokens_salida", 0))
    limpio["latencia_ms"] = int(limpio.get("latencia_ms", 0))
    limpio["coste_estimado_eur"] = float(limpio.get("coste_estimado_eur", 0.0))

    faltan = CAMPOS_REQUERIDOS.difference(limpio.keys())
    if faltan:
        raise ValueError(f"Evento incompleto, faltan campos: {sorted(faltan)}")

    return limpio
