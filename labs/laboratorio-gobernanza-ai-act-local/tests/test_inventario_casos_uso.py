import unittest
from pathlib import Path

from gobernanza.inventario_casos_uso import cargar_casos, resumir_inventario

from scripts.sembrar_datos import main as sembrar


class TestInventarioCasosUso(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sembrar()

    def test_carga_y_resumen(self):
        casos = cargar_casos(Path("datos/casos_uso_ia.json"))
        resumen = resumir_inventario(casos)
        self.assertGreater(resumen["total"], 0)


if __name__ == "__main__":
    unittest.main()
