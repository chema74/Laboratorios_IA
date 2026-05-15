"""Punto de entrada local para demo del generador de escenarios."""

from __future__ import annotations

import sys
from pathlib import Path

# Paso 1: insertar src para ejecución local sin instalación.
RUTA_BASE = Path(__file__).resolve().parent
RUTA_SRC = RUTA_BASE / "src"
if str(RUTA_SRC) not in sys.path:
    sys.path.insert(0, str(RUTA_SRC))

# Paso 2: reutilizar CLI del módulo para concentrar lógica.
from generador_escenarios_prueba_agentes.cli import main

if __name__ == "__main__":
    # Paso 3: ejecutar generación y exportación de escenarios.
    main()
