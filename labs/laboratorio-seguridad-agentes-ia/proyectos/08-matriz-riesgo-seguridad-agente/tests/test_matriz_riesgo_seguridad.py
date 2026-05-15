import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

BASE = Path("proyectos/08-matriz-riesgo-seguridad-agente")
MOD = BASE / "src/matriz_riesgo_seguridad.py"
spec = importlib.util.spec_from_file_location("mr", MOD)
mr = importlib.util.module_from_spec(spec)
assert spec is not None and spec.loader is not None
spec.loader.exec_module(mr)


class TestMatrizRiesgoSeguridad(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sc = BASE / "datos_ejemplo/escenarios_riesgo_seguridad.json"
        cls.cfg = BASE / "datos_ejemplo/configuracion_matriz_seguridad.json"

    def test_existen_archivos(self):
        self.assertTrue(self.sc.exists())
        self.assertTrue(self.cfg.exists())

    def test_cargas(self):
        self.assertTrue(len(mr.cargar_json(self.sc)) > 0)
        self.assertTrue(isinstance(mr.cargar_json(self.cfg), dict))

    def test_calculo_matriz_y_niveles(self):
        r = mr.procesar(mr.cargar_json(self.sc), mr.cargar_json(self.cfg))
        self.assertGreater(r["total_escenarios_evaluados"], 0)
        self.assertTrue(len(r["matriz_probabilidad_x_impacto"]) >= 1)
        self.assertTrue(all(x["nivel_riesgo"] in {"bajo", "medio", "alto", "critico"} for x in r["resultados"]))

    def test_critico_baja_detectabilidad_controles(self):
        r = mr.procesar(mr.cargar_json(self.sc), mr.cargar_json(self.cfg))
        self.assertGreaterEqual(len(r["riesgos_criticos"]), 1)
        self.assertGreaterEqual(len(r["riesgos_baja_detectabilidad"]), 1)
        self.assertGreaterEqual(len(r["riesgos_controles_insuficientes"]), 1)

    def test_genera_salidas(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            md = d / "informe.md"
            js = d / "resultado.json"
            mr.ejecutar(self.sc, self.cfg, md, js)
            self.assertTrue(md.exists())
            self.assertTrue(js.exists())
            self.assertTrue(json.loads(js.read_text(encoding="utf-8")))

    def test_no_uso_reales(self):
        for x in mr.cargar_json(self.sc):
            self.assertFalse(x["usa_datos_reales"])
            self.assertFalse(x["usa_ia_real"])
            self.assertFalse(x["usa_api_externa"])
            self.assertFalse(x["usa_cloud"])


if __name__ == "__main__":
    unittest.main()
