import json
import importlib.util
import tempfile
import unittest
from pathlib import Path

BASE = Path("proyectos/10-demo-seguridad-agentes-completa")
MOD = BASE / "src/demo_seguridad_agentes.py"
spec = importlib.util.spec_from_file_location("d", MOD)
d = importlib.util.module_from_spec(spec)
assert spec is not None and spec.loader is not None
spec.loader.exec_module(d)


class TestDemoSeguridadAgentes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sc = BASE / "datos_ejemplo/escenario_seguridad_agentes.json"
        cls.cfg = BASE / "datos_ejemplo/configuracion_demo_seguridad.json"

    def test_existen_archivos(self):
        self.assertTrue(self.sc.exists())
        self.assertTrue(self.cfg.exists())

    def test_cargas(self):
        self.assertTrue(isinstance(d.cargar_json(self.sc), dict))
        self.assertTrue(isinstance(d.cargar_json(self.cfg), dict))

    def test_demo_outputs(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "demo"
            res = d.ejecutar(self.sc, self.cfg, out)
            self.assertTrue(out.exists())
            self.assertTrue((out / "guion_demo_seguridad_agentes.md").exists())
            self.assertTrue((out / "expediente_seguridad_agentes.md").exists())
            self.assertTrue((out / "demo_seguridad_agentes.json").exists())
            self.assertTrue((out / "mapa_controles_defensivos.md").exists())
            self.assertEqual(len(res["modulos_referenciados"]), 10)

    def test_restricciones(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "demo"
            d.ejecutar(self.sc, self.cfg, out)
            data = json.loads((out / "demo_seguridad_agentes.json").read_text(encoding="utf-8"))
            self.assertFalse(data["usa_datos_reales"])
            self.assertFalse(data["usa_ia_real"])
            self.assertFalse(data["usa_api_externa"])
            self.assertFalse(data["usa_cloud"])
            self.assertFalse(data["usa_herramienta_real"])
            self.assertNotIn("explotar", json.dumps(data, ensure_ascii=False).lower())


if __name__ == "__main__":
    unittest.main()
