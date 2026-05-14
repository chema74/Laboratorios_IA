"""Punto de entrada local para demo del comparador agente-proceso."""

from __future__ import annotations

import sys
from pathlib import Path

# Paso 1: añadir src al path para ejecución local simple.
RUTA_BASE = Path(__file__).resolve().parent
RUTA_SRC = RUTA_BASE / "src"
if str(RUTA_SRC) not in sys.path:
    sys.path.insert(0, str(RUTA_SRC))

# Paso 2: reutilizar la CLI central del módulo.
from comparador_agente_proceso.cli import main


if __name__ == "__main__":
    # Paso 3: ejecutar comparación simulada completa.
    main()
