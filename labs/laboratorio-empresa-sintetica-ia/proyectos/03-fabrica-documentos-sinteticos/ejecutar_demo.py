"""Punto de entrada local para demo de la fábrica documental."""

from __future__ import annotations

import sys
from pathlib import Path

# Paso 1: insertar src en sys.path para ejecución local sin instalación.
RUTA_BASE = Path(__file__).resolve().parent
RUTA_SRC = RUTA_BASE / "src"
if str(RUTA_SRC) not in sys.path:
    sys.path.insert(0, str(RUTA_SRC))

# Paso 2: reutilizar la CLI del módulo para concentrar la lógica.
from fabrica_documentos_sinteticos.cli import main

if __name__ == "__main__":
    # Paso 3: ejecutar generación y exportación documental.
    main()
