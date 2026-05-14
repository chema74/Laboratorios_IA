import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from app.config import RUTA_TAREAS
from colas.cola_simulada import ColaSimulada
from colas.procesador_tareas import procesar_pendientes


def main() -> None:
    with RUTA_TAREAS.open("r", encoding="utf-8-sig") as f:
        tareas = json.load(f)
    cola = ColaSimulada(tareas)
    res = procesar_pendientes(cola)
    print(f"Tareas completadas: {len(res['completadas'])}")
    print(f"Tareas fallidas: {len(res['fallidas'])}")
    print(f"Tareas pendientes: {len(res['pendientes'])}")


if __name__ == "__main__":
    main()
