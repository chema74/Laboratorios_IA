from dataclasses import dataclass


@dataclass
class EventoIA:
    id_evento: str
    caso_uso: str
    tipo_operacion: str
    latencia_ms: int
    tokens_entrada_simulados: int
    tokens_salida_simulados: int
    coste_simulado_eur: float
    estado: str
    riesgo: str
    usuario_sintetico: str
    timestamp: str
