import unittest

from servicios.pipeline_rag import ejecutar_pipeline

from scripts.sembrar_datos import main as sembrar


class TestPipelineRag(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sembrar()

    def test_respuesta_con_citas(self):
        salida = ejecutar_pipeline("Cuál es el SLA de incidencias críticas")
        self.assertIn("respuesta", salida)
        self.assertTrue(salida["citas"])


if __name__ == "__main__":
    unittest.main()
