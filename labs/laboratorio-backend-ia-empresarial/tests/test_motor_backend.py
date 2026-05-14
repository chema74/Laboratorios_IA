import unittest

from app.config import RUTA_PETICIONES, RUTA_USUARIOS
from scripts.sembrar_datos import main as sembrar
from servicios.motor_backend import ejecutar_lote


class TestMotorBackend(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sembrar()

    def test_respuesta_estructurada_y_auditoria(self):
        r = ejecutar_lote(RUTA_PETICIONES, RUTA_USUARIOS)
        self.assertTrue(r["respuestas"])
        self.assertTrue(r["bitacora"])


if __name__ == "__main__":
    unittest.main()
