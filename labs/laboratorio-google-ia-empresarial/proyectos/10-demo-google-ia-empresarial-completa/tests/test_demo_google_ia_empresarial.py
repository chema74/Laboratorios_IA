import json
import sys
import tempfile
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.demo_google_ia_empresarial import cargar_json, construir_demo, escribir_archivos


class TestDemoGoogleIAEmpresarial(unittest.TestCase):
    def setUp(self):
        self.scenario = BASE_DIR / "datos_ejemplo" / "escenario_google_ia_empresarial.json"
        self.config = BASE_DIR / "datos_ejemplo" / "configuracion_demo_google_ia.json"

    def test_existencia_archivos(self):
        self.assertTrue(self.scenario.exists())
        self.assertTrue(self.config.exists())

    def test_demo_outputs(self):
        s = cargar_json(self.scenario)
        c = cargar_json(self.config)
        d = construir_demo(s, c)
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "demo"
            escribir_archivos(d, out)
            self.assertTrue(out.exists())
            self.assertTrue((out / "guion_demo_google_ia_empresarial.md").exists())
            self.assertTrue((out / "expediente_google_ia_empresarial.md").exists())
            self.assertTrue((out / "demo_google_ia_empresarial.json").exists())
            self.assertTrue((out / "mapa_componentes_google_ia.md").exists())
            demo_json = json.loads((out / "demo_google_ia_empresarial.json").read_text(encoding="utf-8"))
            self.assertEqual(len(demo_json["recorrido_modulos"]), 10)
            self.assertFalse(demo_json["usa_google_real"])
            self.assertFalse(demo_json["usa_oauth_real"])
            self.assertFalse(demo_json["usa_api_externa"])
            self.assertFalse(demo_json["usa_cloud"])
            self.assertFalse(demo_json["usa_ia_real"])
            self.assertFalse(demo_json["usa_datos_reales"])


if __name__ == "__main__":
    unittest.main()
