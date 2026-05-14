import json
import sys
import tempfile
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.demo_microsoft_ia_empresarial import cargar_json, ejecutar


class TestDemoMicrosoftIAEmpresarial(unittest.TestCase):
    def setUp(self):
        self.base = BASE_DIR
        self.scenario = self.base / "datos_ejemplo" / "escenario_microsoft_ia_empresarial.json"
        self.config = self.base / "datos_ejemplo" / "configuracion_demo_microsoft_ia.json"

    def test_existen_archivos(self):
        self.assertTrue(self.scenario.exists())
        self.assertTrue(self.config.exists())

    def test_carga_archivos(self):
        s = cargar_json(self.scenario)
        c = cargar_json(self.config)
        self.assertIn("empresa_ficticia", s)
        self.assertIn("modulos_representados", c)

    def test_ejecucion_completa(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "demo"
            salida = ejecutar(self.scenario, self.config, out)
            self.assertTrue(out.exists())
            self.assertTrue((out / "guion_demo_microsoft_ia_empresarial.md").exists())
            self.assertTrue((out / "expediente_microsoft_ia_empresarial.md").exists())
            self.assertTrue((out / "demo_microsoft_ia_empresarial.json").exists())
            self.assertTrue((out / "mapa_componentes_microsoft_ia.md").exists())
            self.assertEqual(len(salida["modulos_representados"]), 10)
            self.assertFalse(salida["usa_microsoft_real"])
            self.assertFalse(salida["usa_microsoft_graph_real"])
            self.assertFalse(salida["usa_oauth_real"])
            self.assertFalse(salida["usa_api_externa"])
            self.assertFalse(salida["usa_azure"])
            self.assertFalse(salida["usa_ia_real"])
            self.assertFalse(salida["usa_datos_reales"])
            contenido = json.loads((out / "demo_microsoft_ia_empresarial.json").read_text(encoding="utf-8"))
            self.assertEqual(len(contenido["modulos_representados"]), 10)


if __name__ == "__main__":
    unittest.main()
