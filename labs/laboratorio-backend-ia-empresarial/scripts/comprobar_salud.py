import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from app.config import RUTA_CONTRATOS, RUTA_INFORME, RUTA_MODULOS, RUTA_PETICIONES, RUTA_TAREAS, RUTA_USUARIOS


def _ok_json(path):
    with path.open("r", encoding="utf-8-sig") as f:
        d = json.load(f)
    return len(d) > 0


def main() -> None:
    checks = []
    for p in [RUTA_CONTRATOS, RUTA_USUARIOS, RUTA_PETICIONES, RUTA_TAREAS, RUTA_MODULOS]:
        checks.append((p.name, p.exists()))
        if p.exists():
            checks.append((f"carga {p.name}", _ok_json(p)))

    checks.append(("modulo motor", (BASE / "servicios" / "motor_backend.py").exists()))
    checks.append(("modulo contratos", (BASE / "api" / "validacion_contratos.py").exists()))
    checks.append(("informe demo", RUTA_INFORME.exists()))

    fallos = [n for n, ok in checks if not ok]
    for n, ok in checks:
        print(f"[{'OK' if ok else 'FAIL'}] {n}")
    if fallos:
        raise SystemExit(f"Salud fallida: {', '.join(fallos)}")
    print("Chequeo de salud correcto.")


if __name__ == "__main__":
    main()
