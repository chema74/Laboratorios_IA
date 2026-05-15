import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

BASE = Path("proyectos/01-inventario-riesgos-agentes")
MOD_PATH = BASE / "src/inventario_riesgos.py"
spec = importlib.util.spec_from_file_location("inventario_riesgos", MOD_PATH)
inventario = importlib.util.module_from_spec(spec)
assert spec is not None and spec.loader is not None
spec.loader.exec_module(inventario)


class TestInventarioRiesgos(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.riesgos_path = BASE / "datos_ejemplo/riesgos_agentes_sinteticos.json"
        cls.config_path = BASE / "datos_ejemplo/configuracion_inventario_riesgos.json"

    def test_existen_archivos_json(self):
        self.assertTrue(self.riesgos_path.exists())
        self.assertTrue(self.config_path.exists())

    def test_carga_datos(self):
        riesgos = inventario.cargar_json(self.riesgos_path)
        config = inventario.cargar_json(self.config_path)
        self.assertTrue(isinstance(riesgos, list) and len(riesgos) > 0)
        self.assertTrue(isinstance(config, dict))

    def test_valida_estructura(self):
        riesgos = inventario.cargar_json(self.riesgos_path)
        self.assertEqual([], inventario.validar_estructura_riesgo(riesgos[0]))

    def test_calcula_puntuacion_y_nivel(self):
        riesgos = inventario.cargar_json(self.riesgos_path)
        config = inventario.cargar_json(self.config_path)
        p = inventario.calcular_puntuacion_riesgo(riesgos[0], config)
        self.assertGreater(p, 0)
        n = inventario.asignar_nivel_riesgo(p, config)
        self.assertIn(n, {"bajo", "medio", "alto", "critico"})

    def test_detecta_critico_y_baja_detectabilidad(self):
        riesgos = inventario.cargar_json(self.riesgos_path)
        config = inventario.cargar_json(self.config_path)
        resultado = inventario.inventariar_riesgos(riesgos, config)
        self.assertGreaterEqual(len(resultado["riesgos_criticos"]), 1)
        self.assertGreaterEqual(len(resultado["riesgos_baja_detectabilidad"]), 1)

    def test_genera_informe_y_json(self):
        with tempfile.TemporaryDirectory() as d:
            md = Path(d) / "informe.md"
            js = Path(d) / "salida.json"
            inventario.ejecutar(self.riesgos_path, self.config_path, md, js)
            self.assertTrue(md.exists())
            self.assertTrue(js.exists())
            self.assertTrue(json.loads(js.read_text(encoding="utf-8")))

    def test_no_usa_reales(self):
        riesgos = inventario.cargar_json(self.riesgos_path)
        for r in riesgos:
            self.assertFalse(r["usa_datos_reales"])
            self.assertFalse(r["usa_ia_real"])
            self.assertFalse(r["usa_api_externa"])
            self.assertFalse(r["usa_cloud"])


if __name__ == "__main__":
    unittest.main()
