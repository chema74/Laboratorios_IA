import unittest

from evaluadores.consistencia import evaluar_consistencia


class TestConsistencia(unittest.TestCase):
    def test_coincidencia_parcial(self):
        out = evaluar_consistencia("plazo 24 horas respuesta", "respuesta en 24 horas")
        self.assertGreater(out["puntuacion"], 0)
        self.assertLess(out["puntuacion"], 1)


if __name__ == "__main__":
    unittest.main()
