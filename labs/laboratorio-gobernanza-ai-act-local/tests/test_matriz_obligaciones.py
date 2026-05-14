import unittest

from gobernanza.matriz_obligaciones import obligaciones_por_riesgo


class TestMatrizObligaciones(unittest.TestCase):
    def test_obligaciones_aplicables(self):
        mapa = {"riesgo limitado": ["trazabilidad"]}
        out = obligaciones_por_riesgo("riesgo limitado", mapa)
        self.assertIn("trazabilidad", out)


if __name__ == "__main__":
    unittest.main()
