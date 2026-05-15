import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

BASE = Path("proyectos/04-clasificador-datos-sensibles-sinteticos")
MOD_PATH = BASE / "src/clasificador_datos_sensibles.py"
spec = importlib.util.spec_from_file_location("clasificador", MOD_PATH)
clasificador = importlib.util.module_from_spec(spec)
assert spec is not None and spec.loader is not None
spec.loader.exec_module(clasificador)


class TestClasificadorDatosSensibles(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data_path = BASE / "datos_ejemplo/datos_sensibles_sinteticos.json"
        cls.config_path = BASE / "datos_ejemplo/configuracion_clasificador_sensibilidad.json"

    def test_existen_archivos_json(self):
        self.assertTrue(self.data_path.exists())
        self.assertTrue(self.config_path.exists())

    def test_carga_datos_y_config(self):
        datos = clasificador.cargar_json(self.data_path)
        config = clasificador.cargar_json(self.config_path)
        self.assertTrue(isinstance(datos, list) and len(datos) > 0)
        self.assertTrue(isinstance(config, dict))

    def test_placeholders_ficticios(self):
        datos = clasificador.cargar_json(self.data_path)
        self.assertTrue(all("[" in d["texto_sintetico"] and "]" in d["texto_sintetico"] for d in datos))

    def test_clasificacion_sensibilidad(self):
        datos = clasificador.cargar_json(self.data_path)
        config = clasificador.cargar_json(self.config_path)
        resultado = clasificador.ejecutar_clasificacion(datos, config)
        self.assertGreater(resultado["total_registros_analizados"], 0)
        tipos = {r["sensibilidad_detectada"] for r in resultado["resultados"]}
        self.assertIn("secreto ficticio", tipos)
        self.assertIn("credencial ficticia", tipos)

    def test_enmascarado_minimizacion_revision(self):
        datos = clasificador.cargar_json(self.data_path)
        config = clasificador.cargar_json(self.config_path)
        resultado = clasificador.ejecutar_clasificacion(datos, config)
        self.assertGreaterEqual(len(resultado["registros_minimizacion"]), 1)
        self.assertGreaterEqual(len(resultado["registros_revision_humana"]), 1)
        self.assertTrue(all("[DATO_ENMASCARADO]" in r["texto_enmascarado_simulado"] for r in resultado["resultados"]))

    def test_genera_informe_y_json(self):
        with tempfile.TemporaryDirectory() as d:
            md = Path(d) / "informe.md"
            js = Path(d) / "resultado.json"
            clasificador.ejecutar(self.data_path, self.config_path, md, js)
            self.assertTrue(md.exists())
            self.assertTrue(js.exists())
            self.assertTrue(json.loads(js.read_text(encoding="utf-8")))

    def test_no_uso_reales(self):
        datos = clasificador.cargar_json(self.data_path)
        for d in datos:
            self.assertFalse(d["usa_datos_reales"])
            self.assertFalse(d["usa_ia_real"])
            self.assertFalse(d["usa_api_externa"])
            self.assertFalse(d["usa_cloud"])


if __name__ == "__main__":
    unittest.main()
