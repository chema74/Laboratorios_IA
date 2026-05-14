import unittest

from app.config import RUTA_INFORME
from scripts.sembrar_datos import main as sembrar
from servicios.generador_informes import generar_informe
from servicios.motor_observabilidad import ejecutar_motor_observabilidad


class TestMotorObservabilidad(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sembrar()

    def test_estructura_e_informe(self):
        r = ejecutar_motor_observabilidad()
        self.assertIn("costes", r)
        self.assertIn("latencias", r)
        ruta = generar_informe(r, RUTA_INFORME)
        self.assertTrue(ruta.exists())


if __name__ == "__main__":
    unittest.main()
