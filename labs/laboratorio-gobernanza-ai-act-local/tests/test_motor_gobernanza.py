import unittest

from app.config import RUTA_FICHAS, RUTA_INFORME
from scripts.sembrar_datos import main as sembrar
from servicios.generador_informes import generar_informe
from servicios.motor_gobernanza import ejecutar_motor


class TestMotorGobernanza(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sembrar()

    def test_genera_informe_y_fichas(self):
        r = ejecutar_motor()
        ruta, fichas = generar_informe(r, RUTA_INFORME, RUTA_FICHAS)
        self.assertTrue(ruta.exists())
        self.assertGreater(len(fichas), 0)


if __name__ == "__main__":
    unittest.main()
