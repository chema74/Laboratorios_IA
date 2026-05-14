import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from app.config import RUTA_RESULTADOS
from servicios.generador_informes import generar_informe_markdown
from servicios.motor_evaluacion import ejecutar_motor


def main() -> None:
    resultado = ejecutar_motor()
    ruta = generar_informe_markdown(resultado, RUTA_RESULTADOS / "informe_evaluacion_llm.md")
    print(f"Evaluación completa finalizada. Informe: {ruta}")


if __name__ == "__main__":
    main()
