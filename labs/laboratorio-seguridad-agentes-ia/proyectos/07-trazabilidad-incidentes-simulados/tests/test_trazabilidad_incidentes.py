import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

BASE = Path("proyectos/07-trazabilidad-incidentes-simulados")
MOD = BASE / "src/trazabilidad_incidentes.py"
spec = importlib.util.spec_from_file_location("trz", MOD)
trz = importlib.util.module_from_spec(spec)
assert spec is not None and spec.loader is not None
spec.loader.exec_module(trz)


class TestTrazabilidadIncidentes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inc = BASE / "datos_ejemplo/incidentes_seguridad_simulados.json"
        cls.cfg = BASE / "datos_ejemplo/configuracion_trazabilidad_incidentes.json"

    def test_existen_archivos(self):
        self.assertTrue(self.inc.exists())
        self.assertTrue(self.cfg.exists())

    def test_cargas(self):
        self.assertTrue(len(trz.cargar_json(self.inc)) > 0)
        self.assertTrue(isinstance(trz.cargar_json(self.cfg), dict))

    def test_evidencia_hash_registros(self):
        with tempfile.TemporaryDirectory() as d:
            r = trz.procesar(trz.cargar_json(self.inc), trz.cargar_json(self.cfg), Path(d))
            self.assertGreaterEqual(len(r["evidencias_generadas"]), 1)
            self.assertTrue(all(len(x["hash_simulado"]) > 0 for x in r["resultados"]))
            self.assertTrue(any(Path(d).glob("*.json")))

    def test_trazabilidad_debil_y_controles(self):
        with tempfile.TemporaryDirectory() as d:
            r = trz.procesar(trz.cargar_json(self.inc), trz.cargar_json(self.cfg), Path(d))
            self.assertGreaterEqual(len(r["incidentes_trazabilidad_debil"]), 1)
            self.assertGreaterEqual(len(r["incidentes_sin_controles_suficientes"]), 1)

    def test_genera_salidas(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            md = d / "informe.md"
            js = d / "resultado.json"
            reg = d / "regs"
            trz.ejecutar(self.inc, self.cfg, md, js, reg)
            self.assertTrue(md.exists())
            self.assertTrue(js.exists())
            self.assertTrue(json.loads(js.read_text(encoding="utf-8")))

    def test_no_uso_reales(self):
        for x in trz.cargar_json(self.inc):
            self.assertFalse(x["usa_datos_reales"])
            self.assertFalse(x["usa_ia_real"])
            self.assertFalse(x["usa_api_externa"])
            self.assertFalse(x["usa_cloud"])


if __name__ == "__main__":
    unittest.main()
