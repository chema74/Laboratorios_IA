import json
import sys
import tempfile
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.generador_informe_google_ia import cargar_json, construir_resultado, generar_md


class TestGeneradorInformeGoogleIA(unittest.TestCase):
    def setUp(self):
        self.results = BASE_DIR / "datos_ejemplo" / "resultados_google_ia_empresarial.json"
        self.config = BASE_DIR / "datos_ejemplo" / "configuracion_informe_google_ia.json"

    def test_existencia_archivos(self):
        self.assertTrue(self.results.exists())
        self.assertTrue(self.config.exists())

    def test_generacion(self):
        r = cargar_json(self.results)
        c = cargar_json(self.config)
        out = construir_resultado(r, c)
        self.assertIn("puntuacion_global", out)
        self.assertIn("nivel_madurez", out)
        self.assertTrue(out["riesgos"])
        self.assertTrue(out["recomendaciones"])
        with tempfile.TemporaryDirectory() as tmp:
            t = Path(tmp)
            md = t / "informe.md"
            js = t / "informe.json"
            generar_md(out, md)
            js.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
            self.assertTrue(md.exists())
            self.assertTrue(js.exists())
        for m in r["modulos"].values():
            self.assertFalse(m["usa_google_real"])
            self.assertFalse(m["usa_oauth_real"])
            self.assertFalse(m["usa_api_externa"])
            self.assertFalse(m["usa_cloud"])
            self.assertFalse(m["usa_ia_real"])
            self.assertFalse(m["usa_datos_reales"])


if __name__ == "__main__":
    unittest.main()
