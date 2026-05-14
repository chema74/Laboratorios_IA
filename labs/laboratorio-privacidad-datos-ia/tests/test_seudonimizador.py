import unittest

from privacidad.seudonimizador import seudonimizar_texto


class TestSeudonimizador(unittest.TestCase):
    def test_ids_estables_en_ejecucion(self):
        t = "NombreFicticio Uno y NombreFicticio Uno email a@x.local"
        r = seudonimizar_texto(t, ["NombreFicticio Uno"])
        self.assertIn("nombre_001", r["texto_seudonimizado"])
        self.assertEqual(list(r["correspondencia"].values()).count("nombre_001"), 1)


if __name__ == "__main__":
    unittest.main()
