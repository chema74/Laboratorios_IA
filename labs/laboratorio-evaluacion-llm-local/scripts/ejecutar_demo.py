import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from servicios.motor_evaluacion import ejecutar_motor


def main() -> None:
    resultado = ejecutar_motor()
    print("Demo evaluación LLM local")
    print(f"Total respuestas: {resultado['metricas']['total_respuestas']}")
    print(f"Media total: {resultado['metricas']['media_puntuacion_total']}")
    print(f"Casos riesgo: {resultado['metricas']['casos_riesgo']}")
    top = sorted(resultado["evaluaciones"], key=lambda x: x["puntuacion_total"], reverse=True)[:3]
    for t in top:
        print(f"- {t['caso_id']} {t['respuesta_id']} => {t['puntuacion_total']}")


if __name__ == "__main__":
    main()
