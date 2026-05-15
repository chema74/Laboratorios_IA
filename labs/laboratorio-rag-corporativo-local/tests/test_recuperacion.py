import unittest

from componentes.recuperador_hibrido import recuperar_hibrido
from componentes.segmentador import segmentar_documentos


class TestRecuperacion(unittest.TestCase):
    def test_devuelve_resultados_relevantes(self):
        docs = [
            {"id": "D-SLA", "titulo": "SLA soporte", "area": "soporte", "etiquetas": ["sla"], "contenido": "incidencias críticas 30 minutos"},
            {"id": "D-OTRO", "titulo": "compras", "area": "compras", "etiquetas": ["proveedor"], "contenido": "proceso de compra"},
        ]
        frags = segmentar_documentos(docs)
        res = recuperar_hibrido("SLA incidencias críticas", frags, top_k=3)
        self.assertGreaterEqual(len(res), 1)
        self.assertEqual(res[0].fragmento.doc_id, "D-SLA")


if __name__ == "__main__":
    unittest.main()
