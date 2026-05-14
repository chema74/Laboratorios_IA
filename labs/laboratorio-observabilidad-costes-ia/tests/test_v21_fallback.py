from __future__ import annotations

import sys
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
SRC = BASE / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from observabilidad_costes_ia.analisis_local import generar_analisis_fallback


class TestFallbackV21(unittest.TestCase):
    def test_fallback_determinista(self):
        metrica = {
            "total_eventos": 3,
            "coste_total_estimado": 0.9,
            "coste_por_caso_uso": {"a": 0.8, "b": 0.1},
            "tokens_totales": 15000,
            "latencia_media_ms": 2200,
            "tasa_errores": 0.2,
            "eventos_riesgo": 2,
        }
        a1 = generar_analisis_fallback(metrica)
        a2 = generar_analisis_fallback(metrica)
        self.assertEqual(a1, a2)
        self.assertEqual(a1["modo"], "fallback_local")
        self.assertTrue(a1["riesgos_detectados"])


if __name__ == "__main__":
    unittest.main()
