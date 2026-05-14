from __future__ import annotations

import sys
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
SRC = BASE / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from observabilidad_costes_ia.escenarios import ESCENARIOS_PREDEFINIDOS, obtener_escenario


class TestEscenariosV21(unittest.TestCase):
    def test_escenarios_minimos(self):
        self.assertGreaterEqual(len(ESCENARIOS_PREDEFINIDOS), 6)
        for nombre in ESCENARIOS_PREDEFINIDOS:
            eventos = obtener_escenario(nombre)
            self.assertGreater(len(eventos), 0)
            self.assertIn("caso_uso", eventos[0])


if __name__ == "__main__":
    unittest.main()
