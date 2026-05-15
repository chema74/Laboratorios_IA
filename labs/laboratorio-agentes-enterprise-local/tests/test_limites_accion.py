import unittest

from orquestacion.limites_accion import validar_accion


class TestLimitesAccion(unittest.TestCase):
    def test_bloqueo(self):
        ok, _ = validar_accion("borrar_datos")
        self.assertFalse(ok)

    def test_permite_accion_declarada(self):
        ok, motivo = validar_accion("consultar_ticket", {"consultar_ticket": True})
        self.assertTrue(ok)
        self.assertEqual(motivo, "ok")

    def test_bloquea_accion_no_declarada(self):
        ok, motivo = validar_accion("accion_desconocida", {"consultar_ticket": True})
        self.assertFalse(ok)
        self.assertEqual(motivo, "accion no declarada en politicas")


if __name__ == "__main__":
    unittest.main()
