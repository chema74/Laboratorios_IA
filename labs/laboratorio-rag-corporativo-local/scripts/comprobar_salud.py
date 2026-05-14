import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from app.config import RUTA_DATOS_BRUTOS, RUTA_DATASET_DORADO


def main() -> None:
    checks = []
    checks.append(("datos brutos", RUTA_DATOS_BRUTOS.exists()))
    checks.append(("dataset dorado", RUTA_DATASET_DORADO.exists()))

    modulos = [
        BASE / "componentes" / "segmentador.py",
        BASE / "componentes" / "recuperador_hibrido.py",
        BASE / "servicios" / "pipeline_rag.py",
        BASE / "seguridad" / "guardia_entrada.py",
    ]
    for m in modulos:
        checks.append((f"módulo {m.name}", m.exists()))

    if RUTA_DATOS_BRUTOS.exists():
        with RUTA_DATOS_BRUTOS.open("r", encoding="utf-8") as f:
            docs = json.load(f)
        checks.append(("documentos > 0", len(docs) > 0))

    fallos = [n for n, ok in checks if not ok]
    for n, ok in checks:
        print(f"[{'OK' if ok else 'FAIL'}] {n}")

    if fallos:
        raise SystemExit(f"Chequeo de salud fallido: {', '.join(fallos)}")
    print("Chequeo de salud completado correctamente.")


if __name__ == "__main__":
    main()
