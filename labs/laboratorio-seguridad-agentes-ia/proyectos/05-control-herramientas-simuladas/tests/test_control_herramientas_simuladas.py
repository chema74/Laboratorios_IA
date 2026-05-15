import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

BASE = Path("proyectos/05-control-herramientas-simuladas")
MOD = BASE / "src/control_herramientas_simuladas.py"
spec = importlib.util.spec_from_file_location("ctrl", MOD)
ctrl = importlib.util.module_from_spec(spec)
assert spec is not None and spec.loader is not None
spec.loader.exec_module(ctrl)


class TestControlHerramientasSimuladas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.req = BASE / "datos_ejemplo/solicitudes_herramientas_simuladas.json"
        cls.cfg = BASE / "datos_ejemplo/configuracion_control_herramientas.json"

    def test_existen_json(self):
        self.assertTrue(self.req.exists())
        self.assertTrue(self.cfg.exists())

    def test_cargas(self):
        self.assertTrue(len(ctrl.cargar_json(self.req)) > 0)
        self.assertTrue(isinstance(ctrl.cargar_json(self.cfg), dict))

    def test_herramientas_permitidas_y_restringidas(self):
        d = ctrl.cargar_json(self.req)
        c = ctrl.cargar_json(self.cfg)
        hs = [x["herramienta_simulada"] for x in d]
        self.assertTrue(any(h in c["herramientas_permitidas"] for h in hs))
        self.assertTrue(any(h in c["herramientas_restringidas"] for h in hs))

    def test_bloqueo_y_revision(self):
        d = ctrl.cargar_json(self.req)
        c = ctrl.cargar_json(self.cfg)
        with tempfile.TemporaryDirectory() as t:
            r = ctrl.procesar(d, c, Path(t))
            self.assertGreaterEqual(r["resumen_por_decision"].get("bloquear", 0), 1)
            self.assertGreaterEqual(r["resumen_por_decision"].get("revisar", 0), 1)

    def test_registros_e_informes(self):
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            md = t / "informe.md"
            js = t / "resultado.json"
            reg = t / "regs"
            ctrl.ejecutar(self.req, self.cfg, md, js, reg)
            self.assertTrue(md.exists())
            self.assertTrue(js.exists())
            self.assertTrue(any(reg.glob("*.json")))
            self.assertTrue(json.loads(js.read_text(encoding="utf-8")))

    def test_no_uso_real(self):
        for x in ctrl.cargar_json(self.req):
            self.assertFalse(x["usa_herramienta_real"])
            self.assertFalse(x["ejecuta_comando_real"])
            self.assertFalse(x["usa_ia_real"])
            self.assertFalse(x["usa_api_externa"])
            self.assertFalse(x["usa_cloud"])
            self.assertFalse(x["usa_datos_reales"])


if __name__ == "__main__":
    unittest.main()
