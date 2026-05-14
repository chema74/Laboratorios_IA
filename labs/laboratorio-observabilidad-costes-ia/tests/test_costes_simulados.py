import unittest

from observabilidad.costes_simulados import analizar_costes


class TestCostes(unittest.TestCase):
    def test_total_y_por_caso(self):
        eventos = [
            {"caso_uso": "a", "coste_simulado_eur": 0.01},
            {"caso_uso": "a", "coste_simulado_eur": 0.02},
            {"caso_uso": "b", "coste_simulado_eur": 0.03},
        ]
        r = analizar_costes(eventos)
        self.assertAlmostEqual(r["coste_total"], 0.06)
        self.assertIn("a", r["coste_por_caso"])


if __name__ == "__main__":
    unittest.main()
