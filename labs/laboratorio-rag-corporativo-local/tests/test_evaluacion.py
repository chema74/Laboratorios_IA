import unittest

from scripts.sembrar_datos import main as sembrar
from evaluacion.evaluacion_offline import generar_informe, evaluar


class TestEvaluacion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sembrar()

    def test_genera_informe_markdown(self):
        metricas = evaluar()
        ruta = generar_informe(metricas)
        self.assertTrue(ruta.exists())
        self.assertEqual(ruta.suffix, ".md")


if __name__ == "__main__":
    unittest.main()
