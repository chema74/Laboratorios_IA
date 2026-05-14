import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from app.config import RUTA_ESCENARIOS, RUTA_HERRAMIENTAS, RUTA_INFORME_DEMO, RUTA_POLITICAS, RUTA_TAREAS


def _check_json(path):
    with path.open("r", encoding="utf-8-sig") as f:
        return len(json.load(f)) > 0


def main() -> None:
    checks = []
    for p in [RUTA_TAREAS, RUTA_HERRAMIENTAS, RUTA_POLITICAS, RUTA_ESCENARIOS]:
        checks.append((p.name, p.exists()))
        if p.exists():
            checks.append((f"carga {p.name}", _check_json(p)))

    checks.append(("modulo orquestacion", (BASE / "orquestacion" / "motor_orquestacion.py").exists()))
    checks.append(("modulo planificador", (BASE / "agentes" / "agente_planificador.py").exists()))
    checks.append(("informe demo generado", RUTA_INFORME_DEMO.exists()))

    fallos = [n for n, ok in checks if not ok]
    for n, ok in checks:
        print(f"[{'OK' if ok else 'FAIL'}] {n}")
    if fallos:
        raise SystemExit(f"Salud fallida: {', '.join(fallos)}")
    print("Chequeo de salud correcto.")


if __name__ == "__main__":
    main()
