import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from app.config import RUTA_INFORME
from servicios.generador_informes import generar_informe
from servicios.motor_privacidad import ejecutar_motor


def main() -> None:
    r = ejecutar_motor()
    ruta = generar_informe(r, RUTA_INFORME)
    print(f"Informe generado: {ruta}")


if __name__ == "__main__":
    main()
