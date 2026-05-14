import unittest

from privacidad.validador_salida import validar_salida


class TestValidadorSalida(unittest.TestCase):
    def test_marca_revisar_o_bloquear(self):
        r = validar_salida("email fuga a@x.local")
        self.assertIn(r["estado"], {"revisar", "bloquear"})


if __name__ == "__main__":
    unittest.main()
