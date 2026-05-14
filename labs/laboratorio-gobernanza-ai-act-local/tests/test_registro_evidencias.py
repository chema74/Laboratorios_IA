import unittest

from gobernanza.registro_evidencias import validar_evidencias


class TestRegistroEvidencias(unittest.TestCase):
    def test_detecta_faltantes(self):
        out = validar_evidencias("C1", {"C1": {"responsable": "x", "descripcion_funcional": True}})
        self.assertFalse(out["completo"])
        self.assertTrue(out["faltantes"])


if __name__ == "__main__":
    unittest.main()
