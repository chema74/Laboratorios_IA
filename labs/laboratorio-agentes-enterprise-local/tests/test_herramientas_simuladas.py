import unittest

from herramientas.crm_simulado import consultar_cliente


class TestHerramientasSimuladas(unittest.TestCase):
    def test_determinista(self):
        a = consultar_cliente("CLI-001")
        b = consultar_cliente("CLI-001")
        self.assertEqual(a, b)


if __name__ == "__main__":
    unittest.main()
