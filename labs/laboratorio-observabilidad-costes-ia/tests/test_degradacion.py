import unittest

from observabilidad.degradacion import detectar_degradacion


class TestDegradacion(unittest.TestCase):
    def test_alertas(self):
        lat = {"p95_aprox": 1600}
        err = {"tasa_error": 0.25}
        fb = {"satisfaccion_media": 2.5}
        cost = {"coste_medio": 0.04}
        a = detectar_degradacion(lat, err, fb, cost)
        self.assertGreaterEqual(len(a), 3)


if __name__ == "__main__":
    unittest.main()
