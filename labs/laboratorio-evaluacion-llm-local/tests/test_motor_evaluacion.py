import unittest

from app.config import RUTA_RESULTADOS
from servicios.generador_informes import generar_informe_markdown
from servicios.motor_evaluacion import ejecutar_motor

from scripts.sembrar_datos import main as sembrar


class TestMotorEvaluacion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sembrar()

    def test_agregadas_e_informe(self):
        res = ejecutar_motor()
        self.assertIn("metricas", res)
        self.assertGreater(res["metricas"]["total_respuestas"], 0)
        ruta = generar_informe_markdown(res, RUTA_RESULTADOS / "informe_evaluacion_llm.md")
        self.assertTrue(ruta.exists())


if __name__ == "__main__":
    unittest.main()
