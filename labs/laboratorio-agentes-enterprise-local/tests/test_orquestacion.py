import unittest

from orquestacion.motor_orquestacion import ejecutar_escenario

from scripts.sembrar_datos import main as sembrar


class TestOrquestacion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sembrar()

    def test_escenario_completo(self):
        r = ejecutar_escenario("ESC-001")
        self.assertIn("plan", r)
        self.assertIn("ejecucion", r)
        self.assertIn("revision", r)


if __name__ == "__main__":
    unittest.main()
