import unittest

from evaluadores.rubricas import puntuar_rubricas


class TestRubricas(unittest.TestCase):
    def test_rango_0_1(self):
        r = puntuar_rubricas(1.2, -0.1, 0.8, 0.6, 0.9, 0.5)
        for v in r.values():
            self.assertGreaterEqual(v, 0)
            self.assertLessEqual(v, 1)


if __name__ == "__main__":
    unittest.main()
