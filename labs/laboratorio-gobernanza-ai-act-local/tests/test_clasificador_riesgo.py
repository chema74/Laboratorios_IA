import unittest

from gobernanza.clasificador_riesgo import clasificar_caso


class TestClasificadorRiesgo(unittest.TestCase):
    def test_categoria_motivos_advertencias(self):
        r = clasificar_caso({"criticidad": "alta", "grado_automatizacion": "alto", "supervision_humana": "baja", "datos_tratados": "sensibles"})
        self.assertIn("categoria", r)
        self.assertTrue(r["motivos"])
        self.assertTrue(r["advertencias"])


if __name__ == "__main__":
    unittest.main()
