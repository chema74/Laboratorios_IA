"""Punto de entrada local para la demo del generador."""

from __future__ import annotations

import sys
from pathlib import Path

# Paso 1: Añadir src al path para ejecución local sin instalación.
RUTA_BASE = Path(__file__).resolve().parent
RUTA_SRC = RUTA_BASE / "src"
if str(RUTA_SRC) not in sys.path:
    sys.path.insert(0, str(RUTA_SRC))

# Paso 2: Reusar la CLI para mantener un único flujo.
from generador_empresa_sintetica.cli import main

if __name__ == "__main__":
    # Paso 3: Ejecutar la demo local con argumentos CLI.
    main()
