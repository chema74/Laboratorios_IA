import unittest

from agentes.agente_planificador import planificar_tarea


class TestPlanificador(unittest.TestCase):
    def test_pasos_y_herramientas(self):
        p = planificar_tarea({"id_tarea": "T-1"})
        self.assertGreaterEqual(len(p["pasos"]), 3)
        self.assertIn("crm_simulado", p["herramientas"])


if __name__ == "__main__":
    unittest.main()
