import unittest

from evaluadores.alucinaciones_sinteticas import evaluar_alucinaciones


class TestAlucinaciones(unittest.TestCase):
    def test_alerta_cifra_inventada(self):
        out = evaluar_alucinaciones("plazo 24 horas", "plazo 72 horas")
        self.assertGreater(out["riesgo"], 0)
        self.assertTrue(out["alertas"])


if __name__ == "__main__":
    unittest.main()
