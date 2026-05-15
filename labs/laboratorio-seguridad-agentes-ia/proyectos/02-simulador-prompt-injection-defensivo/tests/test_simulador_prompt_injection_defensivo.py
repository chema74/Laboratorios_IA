import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

BASE = Path("proyectos/02-simulador-prompt-injection-defensivo")
MOD_PATH = BASE / "src/simulador_prompt_injection_defensivo.py"
spec = importlib.util.spec_from_file_location("simulador", MOD_PATH)
simulador = importlib.util.module_from_spec(spec)
assert spec is not None and spec.loader is not None
spec.loader.exec_module(simulador)


class TestSimuladorPromptInjectionDefensivo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inputs_path = BASE / "datos_ejemplo/entradas_prompt_injection_sinteticas.json"
        cls.config_path = BASE / "datos_ejemplo/configuracion_simulador_defensivo.json"

    def test_existen_archivos_json(self):
        self.assertTrue(self.inputs_path.exists())
        self.assertTrue(self.config_path.exists())

    def test_carga_entradas_y_config(self):
        entradas = simulador.cargar_json(self.inputs_path)
        config = simulador.cargar_json(self.config_path)
        self.assertTrue(isinstance(entradas, list) and len(entradas) > 0)
        self.assertTrue(isinstance(config, dict))

    def test_placeholders_no_accionables(self):
        entradas = simulador.cargar_json(self.inputs_path)
        for entrada in entradas:
            self.assertTrue(simulador.validar_placeholders(entrada["texto_sintetico_no_accionable"]))

    def test_clasificacion_y_politica(self):
        entradas = simulador.cargar_json(self.inputs_path)
        config = simulador.cargar_json(self.config_path)
        resultado = simulador.simular(entradas, config)
        self.assertGreater(resultado["total_entradas_simuladas"], 0)
        item = resultado["resultados"][0]
        self.assertIn("clasificacion_defensiva", item)
        self.assertIn(item["politica_que_deberia_activarse"], config["politicas_defensivas"])
        self.assertTrue(item["respuesta_segura_esperada"])

    def test_revision_humana(self):
        entradas = simulador.cargar_json(self.inputs_path)
        config = simulador.cargar_json(self.config_path)
        resultado = simulador.simular(entradas, config)
        self.assertGreaterEqual(len(resultado["entradas_revision_humana"]), 1)

    def test_genera_informe_y_json(self):
        with tempfile.TemporaryDirectory() as d:
            md = Path(d) / "informe.md"
            js = Path(d) / "resultado.json"
            resultado = simulador.ejecutar(self.inputs_path, self.config_path, md, js)
            self.assertTrue(md.exists())
            self.assertTrue(js.exists())
            data = json.loads(js.read_text(encoding="utf-8"))
            self.assertEqual(resultado["total_entradas_simuladas"], data["total_entradas_simuladas"])

    def test_no_uso_reales(self):
        entradas = simulador.cargar_json(self.inputs_path)
        for entrada in entradas:
            self.assertFalse(entrada["usa_datos_reales"])
            self.assertFalse(entrada["usa_ia_real"])
            self.assertFalse(entrada["usa_api_externa"])
            self.assertFalse(entrada["usa_cloud"])


if __name__ == "__main__":
    unittest.main()
