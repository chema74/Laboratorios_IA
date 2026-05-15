import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

BASE = Path("proyectos/06-politicas-uso-agente")
MOD = BASE / "src/evaluador_politicas_uso.py"
spec = importlib.util.spec_from_file_location("evalp", MOD)
evalp = importlib.util.module_from_spec(spec)
assert spec is not None and spec.loader is not None
spec.loader.exec_module(evalp)


class TestEvaluadorPoliticasUso(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = BASE / "datos_ejemplo/casos_uso_agente_sinteticos.json"
        cls.policies = BASE / "datos_ejemplo/politicas_uso_agente.json"

    def test_existen_json(self):
        self.assertTrue(self.cases.exists())
        self.assertTrue(self.policies.exists())

    def test_cargas(self):
        self.assertTrue(len(evalp.cargar_json(self.cases)) > 0)
        self.assertTrue(len(evalp.cargar_json(self.policies)) > 0)

    def test_evaluacion_y_politica(self):
        c = evalp.cargar_json(self.cases)
        p = evalp.cargar_json(self.policies)
        with tempfile.TemporaryDirectory() as t:
            r = evalp.evaluar(c, p, Path(t))
            self.assertGreater(r["total_casos_evaluados"], 0)
            self.assertGreaterEqual(len(r["resumen_por_politica"]), 1)
            self.assertGreaterEqual(r["resumen_por_decision"].get("bloquear", 0), 1)
            self.assertGreaterEqual(r["resumen_por_decision"].get("revisar", 0), 1)

    def test_incumplimientos_y_registros(self):
        c = evalp.cargar_json(self.cases)
        p = evalp.cargar_json(self.policies)
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            r = evalp.evaluar(c, p, t)
            self.assertGreaterEqual(len(r["incumplimientos_simulados"]), 1)
            self.assertTrue(any(t.glob("*.json")))

    def test_genera_informe_y_json(self):
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            md = t / "informe.md"
            js = t / "resultado.json"
            reg = t / "regs"
            evalp.ejecutar(self.cases, self.policies, md, js, reg)
            self.assertTrue(md.exists())
            self.assertTrue(js.exists())
            self.assertTrue(json.loads(js.read_text(encoding="utf-8")))

    def test_no_uso_real(self):
        for x in evalp.cargar_json(self.cases):
            self.assertFalse(x["usa_datos_reales"])
            self.assertFalse(x["usa_ia_real"])
            self.assertFalse(x["usa_api_externa"])
            self.assertFalse(x["usa_cloud"])


if __name__ == "__main__":
    unittest.main()
