import unittest

from observabilidad.latencias import analizar_latencias


class TestLatencias(unittest.TestCase):
    def test_media_max_p95(self):
        eventos = [{"latencia_ms": 100}, {"latencia_ms": 200}, {"latencia_ms": 1000}, {"latencia_ms": 1500}]
        r = analizar_latencias(eventos, umbral_lento_ms=900)
        self.assertEqual(r["max"], 1500)
        self.assertGreater(r["media"], 0)
        self.assertGreaterEqual(r["p95_aprox"], 1000)


if __name__ == "__main__":
    unittest.main()
