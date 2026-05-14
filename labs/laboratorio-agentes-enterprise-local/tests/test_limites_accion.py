import unittest

from orquestacion.limites_accion import validar_accion


class TestLimitesAccion(unittest.TestCase):
    def test_bloqueo(self):
        ok, _ = validar_accion("borrar_datos")
        self.assertFalse(ok)


if __name__ == "__main__":
    unittest.main()
