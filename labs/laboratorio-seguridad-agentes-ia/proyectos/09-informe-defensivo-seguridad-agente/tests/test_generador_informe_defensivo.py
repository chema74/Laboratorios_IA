import json
import importlib.util
import tempfile
import unittest
from pathlib import Path

BASE = Path("proyectos/09-informe-defensivo-seguridad-agente")
MOD = BASE / "src/generador_informe_defensivo.py"
spec = importlib.util.spec_from_file_location("g", MOD)
g = importlib.util.module_from_spec(spec)
assert spec is not None and spec.loader is not None
spec.loader.exec_module(g)


class TestGeneradorInformeDefensivo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.res = BASE / "datos_ejemplo/resultados_seguridad_agente.json"
        cls.cfg = BASE / "datos_ejemplo/configuracion_informe_defensivo.json"

    def test_existen_archivos(self):
        self.assertTrue(self.res.exists())
        self.assertTrue(self.cfg.exists())

    def test_cargas(self):
        self.assertTrue(isinstance(g.cargar_json(self.res), dict))
        self.assertTrue(isinstance(g.cargar_json(self.cfg), dict))

    def test_calculo_informe(self):
        rep = g.evaluar(g.cargar_json(self.res), g.cargar_json(self.cfg))
        self.assertGreater(rep["puntuacion_global"], 0)
        self.assertIn(rep["nivel_madurez"], {"inicial", "basica", "intermedia", "alta"})
        self.assertTrue(isinstance(rep["riesgos_principales"], list))
        self.assertTrue(isinstance(rep["recomendaciones"], list))

    def test_salidas(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            md = d / "informe.md"
            js = d / "informe.json"
            g.ejecutar(self.res, self.cfg, md, js)
            self.assertTrue(md.exists())
            self.assertTrue(js.exists())
            self.assertTrue(json.loads(js.read_text(encoding="utf-8")))

    def test_no_uso_real(self):
        r = g.cargar_json(self.res)
        for k in ("inventario_riesgos", "simulacion_prompt_injection", "detector_entradas_riesgo", "clasificacion_sensibilidad", "control_herramientas", "politicas_uso", "trazabilidad_incidentes", "matriz_riesgo"):
            self.assertFalse(r[k]["usa_datos_reales"])
            self.assertFalse(r[k]["usa_ia_real"])
            self.assertFalse(r[k]["usa_api_externa"])
            self.assertFalse(r[k]["usa_cloud"])
            self.assertFalse(r[k]["usa_herramienta_real"])


if __name__ == "__main__":
    unittest.main()
