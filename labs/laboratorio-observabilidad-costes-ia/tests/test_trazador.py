import unittest

from observabilidad.trazador import registrar_eventos, resumir_eventos


class TestTrazador(unittest.TestCase):
    def test_carga_y_resumen(self):
        eventos = [{"estado": "ok"}, {"estado": "error"}]
        reg = registrar_eventos(eventos)
        res = resumir_eventos(eventos)
        self.assertEqual(reg["total"], 2)
        self.assertEqual(res["por_estado"]["ok"], 1)


if __name__ == "__main__":
    unittest.main()
