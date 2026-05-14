import unittest

from gobernanza.shadow_ia import analizar_shadow_ia


class TestShadowIA(unittest.TestCase):
    def test_identifica_no_documentados(self):
        out = analizar_shadow_ia([{"id": "S1", "declarado": False, "documentacion": "baja", "impacto": "alto"}])
        self.assertEqual(len(out), 1)


if __name__ == "__main__":
    unittest.main()
