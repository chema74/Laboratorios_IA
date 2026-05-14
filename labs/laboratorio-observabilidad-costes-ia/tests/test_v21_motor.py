from __future__ import annotations

import sys
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
SRC = BASE / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from observabilidad_costes_ia.escenarios import obtener_escenario
from observabilidad_costes_ia.motor import analizar_eventos


class TestMotorV21(unittest.TestCase):
    def test_metricas_agregadas(self):
        eventos = obtener_escenario("uso_normal_controlado")
        r = analizar_eventos(eventos)
        self.assertEqual(r["total_eventos"], 3)
        self.assertGreater(r["coste_total_estimado"], 0)
        self.assertIn("atencion_cliente", r["coste_por_caso_uso"])
        self.assertIn("proveedores_mas_usados", r)

    def test_alertas_por_umbral(self):
        eventos = obtener_escenario("incremento_coste_tokens")
        r = analizar_eventos(eventos)
        tipos = {a["tipo"] for a in r["alertas"]}
        self.assertIn("coste_alto", tipos)
        self.assertIn("exceso_tokens", tipos)


if __name__ == "__main__":
    unittest.main()
