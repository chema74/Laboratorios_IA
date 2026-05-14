import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from app.config import RUTA_DATASET, RUTA_PROMPTS, RUTA_RESPUESTAS


def main() -> None:
    checks = []
    for p in [RUTA_DATASET, RUTA_RESPUESTAS, RUTA_PROMPTS]:
        checks.append((p.name, p.exists()))

    for p in [BASE / "servicios" / "motor_evaluacion.py", BASE / "evaluadores" / "rubricas.py"]:
        checks.append((p.name, p.exists()))

    for p in [RUTA_DATASET, RUTA_RESPUESTAS, RUTA_PROMPTS]:
        if p.exists():
            with p.open("r", encoding="utf-8-sig") as f:
                data = json.load(f)
            checks.append((f"carga {p.name}", len(data) > 0))

    fallos = [n for n, ok in checks if not ok]
    for n, ok in checks:
        print(f"[{'OK' if ok else 'FAIL'}] {n}")
    if fallos:
        raise SystemExit(f"Salud fallida: {', '.join(fallos)}")
    print("Chequeo de salud correcto.")


if __name__ == "__main__":
    main()
