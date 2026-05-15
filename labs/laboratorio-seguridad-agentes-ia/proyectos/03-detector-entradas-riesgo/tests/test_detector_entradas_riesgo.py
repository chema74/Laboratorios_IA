import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

BASE = Path("proyectos/03-detector-entradas-riesgo")
MOD_PATH = BASE / "src/detector_entradas_riesgo.py"
spec = importlib.util.spec_from_file_location("detector", MOD_PATH)
detector = importlib.util.module_from_spec(spec)
assert spec is not None and spec.loader is not None
spec.loader.exec_module(detector)


class TestDetectorEntradasRiesgo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inputs_path = BASE / "datos_ejemplo/entradas_riesgo_sinteticas.json"
        cls.config_path = BASE / "datos_ejemplo/configuracion_detector_riesgo.json"

    def test_existen_archivos_json(self):
        self.assertTrue(self.inputs_path.exists())
        self.assertTrue(self.config_path.exists())

    def test_carga_entradas_y_config(self):
        entradas = detector.cargar_json(self.inputs_path)
        config = detector.cargar_json(self.config_path)
        self.assertTrue(isinstance(entradas, list) and len(entradas) > 0)
        self.assertTrue(isinstance(config, dict))

    def test_placeholders_ficticios(self):
        entradas = detector.cargar_json(self.inputs_path)
        self.assertTrue(all(detector.contiene_placeholder(e["texto_sintetico_no_accionable"]) for e in entradas))

    def test_detecta_categoria_y_severidad(self):
        entradas = detector.cargar_json(self.inputs_path)
        config = detector.cargar_json(self.config_path)
        resultado = detector.ejecutar_analisis(entradas, config)
        self.assertGreater(resultado["total_entradas_analizadas"], 0)
        self.assertIn("categoria_detectada", resultado["resultados"][0])
        self.assertIn("severidad_simulada", resultado["resultados"][0])

    def test_bloqueo_y_revision_humana(self):
        entradas = detector.cargar_json(self.inputs_path)
        config = detector.cargar_json(self.config_path)
        resultado = detector.ejecutar_analisis(entradas, config)
        self.assertGreaterEqual(len(resultado["entradas_bloqueables"]), 1)
        self.assertGreaterEqual(len(resultado["entradas_revision_humana"]), 1)

    def test_genera_informe_y_json(self):
        with tempfile.TemporaryDirectory() as d:
            md = Path(d) / "informe.md"
            js = Path(d) / "resultado.json"
            detector.ejecutar(self.inputs_path, self.config_path, md, js)
            self.assertTrue(md.exists())
            self.assertTrue(js.exists())
            self.assertTrue(json.loads(js.read_text(encoding="utf-8")))

    def test_no_uso_reales(self):
        entradas = detector.cargar_json(self.inputs_path)
        for e in entradas:
            self.assertFalse(e["usa_datos_reales"])
            self.assertFalse(e["usa_ia_real"])
            self.assertFalse(e["usa_api_externa"])
            self.assertFalse(e["usa_cloud"])


if __name__ == "__main__":
    unittest.main()
