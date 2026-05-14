import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from app.config import RUTA_PETICIONES, RUTA_USUARIOS
from servicios.motor_backend import ejecutar_lote


def main() -> None:
    out = ejecutar_lote(RUTA_PETICIONES, RUTA_USUARIOS)
    print("Simulación backend local ejecutada")
    print(f"- Respuestas: {len(out['respuestas'])}")
    print(f"- Registros auditoría: {len(out['bitacora'])}")


if __name__ == "__main__":
    main()
