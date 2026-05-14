import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from app.config import RUTA_DATASET, RUTA_INFORME, RUTA_POLITICAS, RUTA_PROMPTS, RUTA_REGISTRO, RUTA_SALIDAS


def _ok_json(path):
    with path.open("r", encoding="utf-8-sig") as f:
        data = json.load(f)
    return len(data) > 0


def main() -> None:
    checks = []
    for p in [RUTA_DATASET, RUTA_POLITICAS, RUTA_PROMPTS, RUTA_SALIDAS, RUTA_REGISTRO]:
        checks.append((p.name, p.exists()))
        if p.exists():
            checks.append((f"carga {p.name}", _ok_json(p)))

    checks.append(("modulo detector", (BASE / "privacidad" / "detector_pii.py").exists()))
    checks.append(("modulo motor", (BASE / "servicios" / "motor_privacidad.py").exists()))
    checks.append(("informe generado", RUTA_INFORME.exists()))

    fallos = [n for n, ok in checks if not ok]
    for n, ok in checks:
        print(f"[{'OK' if ok else 'FAIL'}] {n}")
    if fallos:
        raise SystemExit(f"Salud fallida: {', '.join(fallos)}")
    print("Chequeo de salud correcto.")


if __name__ == "__main__":
    main()
