import unittest

from evaluadores.regresion_prompts import evaluar_regresion


class TestRegresion(unittest.TestCase):
    def test_detecta_perdida(self):
        out = evaluar_regresion(["2000 euros", "finanzas"], "incluye 2000 euros y finanzas", "incluye 2000 euros")
        self.assertEqual(out["veredicto"], "empeora")


if __name__ == "__main__":
    unittest.main()
