from __future__ import annotations

from copy import deepcopy


def _evento(
    id_evento: str,
    caso_uso: str,
    modelo: str,
    proveedor: str,
    tokens_entrada: int,
    tokens_salida: int,
    latencia_ms: int,
    coste: float,
    estado: str,
    riesgo: str,
    equipo: str,
    usuario: str,
    timestamp: str,
) -> dict[str, object]:
    return {
        "id_evento": id_evento,
        "caso_uso": caso_uso,
        "modelo": modelo,
        "proveedor": proveedor,
        "tokens_entrada": tokens_entrada,
        "tokens_salida": tokens_salida,
        "latencia_ms": latencia_ms,
        "coste_estimado_eur": coste,
        "estado": estado,
        "riesgo": riesgo,
        "equipo": equipo,
        "usuario": usuario,
        "timestamp": timestamp,
        "trazabilidad": f"trace-{id_evento}",
    }


ESCENARIOS_PREDEFINIDOS: dict[str, list[dict[str, object]]] = {
    "uso_normal_controlado": [
        _evento("N-001", "atencion_cliente", "llama-3.1-8b", "local", 500, 220, 620, 0.012, "ok", "bajo", "cx", "ana", "2026-05-12T08:01:00Z"),
        _evento("N-002", "soporte_tic", "llama-3.1-8b", "local", 420, 180, 540, 0.01, "ok", "bajo", "it", "luis", "2026-05-12T08:02:00Z"),
        _evento("N-003", "cumplimiento", "llama-3.1-8b", "local", 650, 260, 700, 0.015, "ok", "medio", "legal", "eva", "2026-05-12T08:03:00Z"),
    ],
    "incremento_coste_tokens": [
        _evento("C-001", "generacion_contratos", "llama-3.1-70b", "groq", 6000, 3200, 1250, 0.38, "ok", "medio", "legal", "mario", "2026-05-12T09:01:00Z"),
        _evento("C-002", "generacion_contratos", "llama-3.1-70b", "groq", 5800, 3000, 1180, 0.36, "ok", "medio", "legal", "mario", "2026-05-12T09:02:00Z"),
        _evento("C-003", "generacion_contratos", "llama-3.1-70b", "groq", 6200, 3500, 1310, 0.41, "ok", "alto", "legal", "mario", "2026-05-12T09:03:00Z"),
    ],
    "alta_latencia_critica": [
        _evento("L-001", "fraude_tiempo_real", "mixtral-8x7b", "local", 1000, 400, 2800, 0.05, "ok", "alto", "riesgos", "sara", "2026-05-12T10:01:00Z"),
        _evento("L-002", "fraude_tiempo_real", "mixtral-8x7b", "local", 1100, 420, 3200, 0.055, "ok", "alto", "riesgos", "sara", "2026-05-12T10:02:00Z"),
        _evento("L-003", "fraude_tiempo_real", "mixtral-8x7b", "local", 950, 390, 2950, 0.049, "ok", "alto", "riesgos", "sara", "2026-05-12T10:03:00Z"),
    ],
    "errores_repetidos_automatizacion": [
        _evento("E-001", "backoffice_facturas", "llama-3.1-8b", "local", 760, 300, 980, 0.021, "error", "medio", "ops", "pepe", "2026-05-12T11:01:00Z"),
        _evento("E-002", "backoffice_facturas", "llama-3.1-8b", "local", 720, 280, 1020, 0.02, "error", "medio", "ops", "pepe", "2026-05-12T11:02:00Z"),
        _evento("E-003", "backoffice_facturas", "llama-3.1-8b", "local", 740, 290, 1010, 0.02, "ok", "bajo", "ops", "pepe", "2026-05-12T11:03:00Z"),
    ],
    "concentracion_consumo_equipo": [
        _evento("Q-001", "analisis_riesgo", "llama-3.1-70b", "groq", 3200, 1100, 1400, 0.19, "ok", "medio", "finanzas", "carlos", "2026-05-12T12:01:00Z"),
        _evento("Q-002", "analisis_riesgo", "llama-3.1-70b", "groq", 3100, 1000, 1350, 0.18, "ok", "medio", "finanzas", "carlos", "2026-05-12T12:02:00Z"),
        _evento("Q-003", "asistente_rrhh", "llama-3.1-8b", "local", 300, 160, 500, 0.008, "ok", "bajo", "rrhh", "ines", "2026-05-12T12:03:00Z"),
    ],
    "riesgo_uso_sensible": [
        _evento("R-001", "screening_rrhh", "llama-3.1-70b", "groq", 2200, 900, 1650, 0.14, "ok", "alto", "rrhh", "julia", "2026-05-12T13:01:00Z"),
        _evento("R-002", "screening_rrhh", "llama-3.1-70b", "groq", 2100, 840, 1580, 0.132, "ok", "alto", "rrhh", "julia", "2026-05-12T13:02:00Z"),
        _evento("R-003", "screening_rrhh", "llama-3.1-8b", "local", 900, 350, 980, 0.022, "ok", "medio", "rrhh", "julia", "2026-05-12T13:03:00Z"),
    ],
}


def obtener_escenario(nombre: str) -> list[dict[str, object]]:
    if nombre not in ESCENARIOS_PREDEFINIDOS:
        raise KeyError(f"Escenario no disponible: {nombre}")
    return deepcopy(ESCENARIOS_PREDEFINIDOS[nombre])
