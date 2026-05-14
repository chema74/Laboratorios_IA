import unittest

from evaluadores.cobertura import evaluar_cobertura


class TestCobertura(unittest.TestCase):
    def test_cubiertos_no_cubiertos(self):
        out = evaluar_cobertura(["24 horas", "finanzas"], "incluye 24 horas")
        self.assertIn("24 horas", out["cubiertos"])
        self.assertIn("finanzas", out["no_cubiertos"])


if __name__ == "__main__":
    unittest.main()
