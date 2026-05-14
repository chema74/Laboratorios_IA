import unittest

from componentes.segmentador import segmentar_documentos


class TestSegmentacion(unittest.TestCase):
    def test_genera_fragmentos_con_referencia(self):
        docs = [{"id": "D1", "titulo": "t", "area": "a", "etiquetas": ["x"], "contenido": "texto largo " * 50}]
        frags = segmentar_documentos(docs, tamano_fragmento=60)
        self.assertGreater(len(frags), 1)
        self.assertEqual(frags[0].doc_id, "D1")
        self.assertTrue(frags[0].fragmento_id.startswith("D1_f"))


if __name__ == "__main__":
    unittest.main()
