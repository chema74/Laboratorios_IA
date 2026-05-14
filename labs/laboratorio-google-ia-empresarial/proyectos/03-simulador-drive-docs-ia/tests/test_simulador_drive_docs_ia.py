import json
import sys
import tempfile
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.simulador_drive_docs_ia import (
    construir_resultado_global,
    cargar_json,
    generar_informe_markdown,
    procesar_documentos,
    validar_documentos,
)


class TestSimuladorDriveDocsIA(unittest.TestCase):
    def setUp(self):
        self.base = BASE_DIR
        self.docs = self.base / "datos_ejemplo" / "documentos_empresariales_sinteticos.json"
        self.config = self.base / "datos_ejemplo" / "configuracion_drive_docs_simulado.json"

    def test_existen_archivos(self):
        self.assertTrue(self.docs.exists())
        self.assertTrue(self.config.exists())

    def test_carga_y_validacion(self):
        data = cargar_json(self.docs)
        cfg = cargar_json(self.config)
        self.assertIn("documentos", data)
        validar_documentos(data["documentos"], cfg)

    def test_procesamiento_e_informes(self):
        data = cargar_json(self.docs)
        cfg = cargar_json(self.config)
        with tempfile.TemporaryDirectory() as tmp:
            tmp_dir = Path(tmp)
            resultados = procesar_documentos(data, cfg, tmp_dir / "documentos")
            self.assertTrue(all(x["resumen_simulado"] for x in resultados))
            self.assertTrue(all(x["etiquetas_simuladas"] for x in resultados))
            self.assertTrue(all(Path(x["registro_generado"]).exists() for x in resultados))
            for item in resultados:
                self.assertFalse(item["usa_drive_real"])
                self.assertFalse(item["usa_docs_real"])
                self.assertFalse(item["usa_oauth_real"])
                self.assertFalse(item["usa_api_externa"])
                self.assertFalse(item["usa_cloud"])
                self.assertFalse(item["usa_ia_real"])
            resumen = construir_resultado_global(resultados, cfg)
            out_json = tmp_dir / "resultado.json"
            out_md = tmp_dir / "informe.md"
            out_json.write_text(json.dumps(resumen, ensure_ascii=False, indent=2), encoding="utf-8")
            generar_informe_markdown(resumen, out_md)
            self.assertTrue(out_json.exists())
            self.assertTrue(out_md.exists())


if __name__ == "__main__":
    unittest.main()
