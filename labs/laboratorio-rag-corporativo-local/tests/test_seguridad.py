import unittest

from seguridad.guardia_entrada import validar_consulta


class TestSeguridad(unittest.TestCase):
    def test_bloquea_vacia(self):
        ok, motivo = validar_consulta("   ")
        self.assertFalse(ok)
        self.assertIn("vacía", motivo)

    def test_bloquea_fuera_dominio(self):
        ok, _ = validar_consulta("dime el horoscopo")
        self.assertFalse(ok)


if __name__ == "__main__":
    unittest.main()
