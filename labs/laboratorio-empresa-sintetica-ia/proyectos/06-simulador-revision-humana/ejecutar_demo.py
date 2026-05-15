"""Punto de entrada local para demo del simulador de revisión humana."""

from __future__ import annotations

import sys
from pathlib import Path

# Paso 1: incluir src en path para ejecución local.
RUTA_BASE = Path(__file__).resolve().parent
RUTA_SRC = RUTA_BASE / "src"
if str(RUTA_SRC) not in sys.path:
    sys.path.insert(0, str(RUTA_SRC))

# Paso 2: reutilizar CLI para centralizar flujo.
from simulador_revision_humana.cli import main

if __name__ == "__main__":
    # Paso 3: ejecutar simulación y exportación.
    main()
