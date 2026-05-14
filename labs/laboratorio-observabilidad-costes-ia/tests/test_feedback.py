import unittest

from observabilidad.feedback import analizar_feedback


class TestFeedback(unittest.TestCase):
    def test_satisfaccion_media(self):
        r = analizar_feedback([
            {"caso_uso": "x", "satisfaccion": 4},
            {"caso_uso": "x", "satisfaccion": 2},
        ])
        self.assertEqual(r["satisfaccion_media"], 3.0)


if __name__ == "__main__":
    unittest.main()
