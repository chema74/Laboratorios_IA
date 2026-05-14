"""Punto de entrada local para demo del gemelo digital operativo."""

from __future__ import annotations

import sys
from pathlib import Path

# Paso 1: agregar src al path para ejecución local simple.
RUTA_BASE = Path(__file__).resolve().parent
RUTA_SRC = RUTA_BASE / "src"
if str(RUTA_SRC) not in sys.path:
    sys.path.insert(0, str(RUTA_SRC))

# Paso 2: reutilizar la CLI para un flujo único.
from gemelo_digital_operativo_ligero.cli import main


if __name__ == "__main__":
    # Paso 3: ejecutar construcción y exportación del estado operativo.
    main()
