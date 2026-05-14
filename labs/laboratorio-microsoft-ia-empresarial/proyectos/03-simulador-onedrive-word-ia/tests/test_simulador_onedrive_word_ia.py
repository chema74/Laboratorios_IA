import json
import sys
import tempfile
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.simulador_onedrive_word_ia import cargar_json, ejecutar, validar_documentos


class TestSimuladorOneDriveWordIA(unittest.TestCase):
    def setUp(self):
        self.base = BASE_DIR
        self.docs_path = self.base / "datos_ejemplo" / "documentos_word_sinteticos.json"
        self.config_path = self.base / "datos_ejemplo" / "configuracion_onedrive_word_simulado.json"

    def test_existen_archivos_base(self):
        self.assertTrue(self.docs_path.exists())
        self.assertTrue(self.config_path.exists())

    def test_carga_documentos_y_config(self):
        data = cargar_json(self.docs_path)
        config = cargar_json(self.config_path)
        self.assertIn("documentos", data)
        self.assertIn("tipos_documento_permitidos", config)

    def test_validacion_documentos(self):
        data = cargar_json(self.docs_path)
        config = cargar_json(self.config_path)
        validar_documentos(data["documentos"], config)

    def test_simulacion_completa(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            out_md = tmp / "informe.md"
            out_json = tmp / "salida.json"
            docs_dir = tmp / "docs"

            resultado = ejecutar(self.docs_path, self.config_path, out_md, out_json, docs_dir)
            self.assertTrue(out_md.exists())
            self.assertTrue(out_json.exists())
            self.assertIn("resumen_por_tipo_documental", resultado)
            self.assertIn("resumen_por_sensibilidad", resultado)

            resultados = resultado["resultados"]
            self.assertGreater(len(resultados), 0)
            self.assertTrue(any(r["requiere_revision_humana"] for r in resultados))
            for r in resultados:
                self.assertTrue(r["resumen_simulado"])
                self.assertTrue(len(r["etiquetas_simuladas"]) > 0)
                self.assertTrue(r["registro_generado"])
                self.assertTrue(Path(r["registro_generado"]).exists())
                self.assertFalse(r["usa_onedrive_real"])
                self.assertFalse(r["usa_word_real"])
                self.assertFalse(r["usa_microsoft_graph_real"])
                self.assertFalse(r["usa_oauth_real"])
                self.assertFalse(r["usa_api_externa"])
                self.assertFalse(r["usa_azure"])
                self.assertFalse(r["usa_ia_real"])

            contenido = json.loads(out_json.read_text(encoding="utf-8"))
            self.assertEqual(contenido["metadata"]["total_documentos"], len(resultados))


if __name__ == "__main__":
    unittest.main()
