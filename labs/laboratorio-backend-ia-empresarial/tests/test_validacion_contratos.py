import unittest

from api.validacion_contratos import validar_peticion


class TestValidacionContratos(unittest.TestCase):
    def test_detecta_incompleta(self):
        r = validar_peticion({"endpoint": "/x"})
        self.assertFalse(r["valida"])
        self.assertTrue(r["errores"])


if __name__ == "__main__":
    unittest.main()
