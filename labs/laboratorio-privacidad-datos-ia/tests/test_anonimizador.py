import unittest

from privacidad.anonimizador import anonimizar_texto


class TestAnonimizador(unittest.TestCase):
    def test_sustituye_marcadores(self):
        t = "NombreFicticio Uno correo n@x.local"
        r = anonimizar_texto(t, ["NombreFicticio Uno"])
        self.assertIn("[NOMBRE]", r["texto_anonimizado"])
        self.assertIn("[EMAIL]", r["texto_anonimizado"])


if __name__ == "__main__":
    unittest.main()
