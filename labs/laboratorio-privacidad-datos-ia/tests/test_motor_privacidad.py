import unittest

from app.config import RUTA_INFORME
from servicios.generador_informes import generar_informe
from servicios.motor_privacidad import ejecutar_motor

from scripts.sembrar_datos import main as sembrar


class TestMotorPrivacidad(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sembrar()

    def test_resultados_e_informe(self):
        r = ejecutar_motor()
        self.assertIn("analisis_casos", r)
        ruta = generar_informe(r, RUTA_INFORME)
        self.assertTrue(ruta.exists())


if __name__ == "__main__":
    unittest.main()
