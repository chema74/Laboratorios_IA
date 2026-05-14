import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
DATOS = BASE / "datos"


def main() -> None:
    DATOS.mkdir(parents=True, exist_ok=True)

    eventos = [
        {"id_evento": "E-001", "caso_uso": "atencion_cliente", "tipo_operacion": "consulta", "latencia_ms": 420, "tokens_entrada_simulados": 210, "tokens_salida_simulados": 120, "coste_simulado_eur": 0.0112, "estado": "ok", "riesgo": "bajo", "usuario_sintetico": "u001", "timestamp": "2025-01-10T10:00:00Z"},
        {"id_evento": "E-002", "caso_uso": "soporte_tic", "tipo_operacion": "clasificacion", "latencia_ms": 1550, "tokens_entrada_simulados": 350, "tokens_salida_simulados": 160, "coste_simulado_eur": 0.038, "estado": "ok", "riesgo": "medio", "usuario_sintetico": "u002", "timestamp": "2025-01-10T10:01:00Z"},
        {"id_evento": "E-003", "caso_uso": "compras", "tipo_operacion": "resumen", "latencia_ms": 980, "tokens_entrada_simulados": 290, "tokens_salida_simulados": 140, "coste_simulado_eur": 0.026, "estado": "error", "tipo_error": "timeout", "riesgo": "alto", "usuario_sintetico": "u003", "timestamp": "2025-01-10T10:02:00Z"},
        {"id_evento": "E-004", "caso_uso": "recursos_humanos", "tipo_operacion": "consulta", "latencia_ms": 610, "tokens_entrada_simulados": 180, "tokens_salida_simulados": 110, "coste_simulado_eur": 0.014, "estado": "ok", "riesgo": "bajo", "usuario_sintetico": "u004", "timestamp": "2025-01-10T10:03:00Z"},
        {"id_evento": "E-005", "caso_uso": "cumplimiento", "tipo_operacion": "validacion", "latencia_ms": 1700, "tokens_entrada_simulados": 410, "tokens_salida_simulados": 170, "coste_simulado_eur": 0.043, "estado": "error", "tipo_error": "datos_incompletos", "riesgo": "alto", "usuario_sintetico": "u005", "timestamp": "2025-01-10T10:04:00Z"},
        {"id_evento": "E-006", "caso_uso": "atencion_cliente", "tipo_operacion": "consulta", "latencia_ms": 530, "tokens_entrada_simulados": 220, "tokens_salida_simulados": 130, "coste_simulado_eur": 0.0126, "estado": "ok", "riesgo": "bajo", "usuario_sintetico": "u006", "timestamp": "2025-01-10T10:05:00Z"}
    ]

    presupuesto = {"mes": "2025-01", "presupuesto_mensual_eur": 0.25, "nota": "Presupuesto ficticio de laboratorio"}

    feedback = [
        {"id_feedback": "F-001", "caso_uso": "atencion_cliente", "satisfaccion": 4, "comentario": "Respuesta útil y rápida"},
        {"id_feedback": "F-002", "caso_uso": "soporte_tic", "satisfaccion": 2, "comentario": "Demasiada latencia"},
        {"id_feedback": "F-003", "caso_uso": "compras", "satisfaccion": 3, "comentario": "Aceptable"},
        {"id_feedback": "F-004", "caso_uso": "cumplimiento", "satisfaccion": 1, "comentario": "Errores frecuentes"}
    ]

    (DATOS / "eventos_ia_sinteticos.json").write_text(json.dumps(eventos, ensure_ascii=False, indent=2), encoding="utf-8")
    (DATOS / "presupuesto_operativo.json").write_text(json.dumps(presupuesto, ensure_ascii=False, indent=2), encoding="utf-8")
    (DATOS / "feedback_usuarios.json").write_text(json.dumps(feedback, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Datos sintéticos de observabilidad creados.")


if __name__ == "__main__":
    main()
