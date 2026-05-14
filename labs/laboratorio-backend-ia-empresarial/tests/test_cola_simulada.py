import unittest

from colas.cola_simulada import ColaSimulada


class TestColaSimulada(unittest.TestCase):
    def test_agrega_lista_completa(self):
        c = ColaSimulada([])
        c.agregar({"id": "1", "tipo": "x"})
        self.assertEqual(len(c.pendientes()), 1)
        self.assertTrue(c.marcar_completada("1"))


if __name__ == "__main__":
    unittest.main()
