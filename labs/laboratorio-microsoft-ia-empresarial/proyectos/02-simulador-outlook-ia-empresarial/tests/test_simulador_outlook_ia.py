import json
import sys
import tempfile
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.simulador_outlook_ia import cargar_json, ejecutar, validar_correos


class TestSimuladorOutlookIA(unittest.TestCase):
    def setUp(self):
        self.base = Path(__file__).resolve().parents[1]
        self.emails_path = self.base / "datos_ejemplo" / "correos_outlook_sinteticos.json"
        self.config_path = self.base / "datos_ejemplo" / "configuracion_outlook_simulado.json"

    def test_existen_archivos_base(self):
        self.assertTrue(self.emails_path.exists())
        self.assertTrue(self.config_path.exists())

    def test_carga_correos_y_config(self):
        data = cargar_json(self.emails_path)
        config = cargar_json(self.config_path)
        self.assertIn("correos", data)
        self.assertIn("reglas_clasificacion", config)

    def test_validacion_correos(self):
        data = cargar_json(self.emails_path)
        config = cargar_json(self.config_path)
        validar_correos(data["correos"], config)

    def test_simulacion_completa(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            out_md = tmp / "informe.md"
            out_json = tmp / "salida.json"
            mailbox = tmp / "mailbox"

            resultado = ejecutar(self.emails_path, self.config_path, out_md, out_json, mailbox)
            self.assertTrue(out_md.exists())
            self.assertTrue(out_json.exists())
            self.assertIn("resumen_por_carpeta", resultado)
            self.assertIn("resumen_por_categoria", resultado)
            self.assertIn("resumen_por_prioridad", resultado)

            resultados = resultado["resultados"]
            self.assertGreater(len(resultados), 0)
            self.assertTrue(any(r["requiere_respuesta"] for r in resultados))
            self.assertTrue(any(r["requiere_tarea"] for r in resultados))
            self.assertTrue(any(r["requiere_reunion"] for r in resultados))

            for r in resultados:
                self.assertTrue(r["registro_generado"])
                self.assertFalse(r["usa_outlook_real"])
                self.assertFalse(r["usa_microsoft_graph_real"])
                self.assertFalse(r["usa_oauth_real"])
                self.assertFalse(r["usa_api_externa"])
                self.assertFalse(r["usa_azure"])
                self.assertFalse(r["usa_ia_real"])
                self.assertTrue(Path(r["registro_generado"]).exists())

            contenido = json.loads(out_json.read_text(encoding="utf-8"))
            self.assertEqual(contenido["metadata"]["total_correos"], len(resultados))


if __name__ == "__main__":
    unittest.main()
