import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from app.config import RUTA_EVENTOS, RUTA_FEEDBACK, RUTA_INFORME, RUTA_PANEL, RUTA_PRESUPUESTO


def main() -> None:
    checks = []
    for p in [RUTA_EVENTOS, RUTA_PRESUPUESTO, RUTA_FEEDBACK]:
        checks.append((p.name, p.exists()))
        if p.exists():
            with p.open("r", encoding="utf-8-sig") as f:
                checks.append((f"carga {p.name}", len(json.load(f)) > 0))

    for p in [BASE / "servicios" / "motor_observabilidad.py", BASE / "observabilidad" / "latencias.py"]:
        checks.append((p.name, p.exists()))

    checks.append(("informe generado", RUTA_INFORME.exists()))
    checks.append(("panel generado", RUTA_PANEL.exists()))

    fallos = [n for n, ok in checks if not ok]
    for n, ok in checks:
        print(f"[{'OK' if ok else 'FAIL'}] {n}")
    if fallos:
        raise SystemExit(f"Salud fallida: {', '.join(fallos)}")
    print("Chequeo de salud correcto.")


if __name__ == "__main__":
    main()
