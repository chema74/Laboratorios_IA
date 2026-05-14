import json
import sys
import tempfile
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.generador_informe_microsoft_ia import cargar_json, ejecutar


class TestGeneradorInformeMicrosoftIA(unittest.TestCase):
    def setUp(self):
        self.base = BASE_DIR
        self.results = self.base / "datos_ejemplo" / "resultados_microsoft_ia_empresarial.json"
        self.config = self.base / "datos_ejemplo" / "configuracion_informe_microsoft_ia.json"

    def test_existen_archivos(self):
        self.assertTrue(self.results.exists())
        self.assertTrue(self.config.exists())

    def test_carga_datos(self):
        r = cargar_json(self.results)
        c = cargar_json(self.config)
        self.assertIn("modulos_resultados", r)
        self.assertIn("dimensiones_evaluacion", c)

    def test_ejecucion_completa(self):
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            out_md = td_path / "informe.md"
            out_json = td_path / "informe.json"
            salida = ejecutar(self.results, self.config, out_md, out_json)
            self.assertTrue(out_md.exists())
            self.assertTrue(out_json.exists())
            self.assertIn("puntuacion_global_simulada", salida)
            self.assertIn("nivel_madurez_simulado", salida)
            self.assertIn(salida["nivel_madurez_simulado"], {"inicial", "básico", "intermedio", "alto"})
            self.assertTrue(len(salida["riesgos_principales"]) > 0)
            self.assertTrue(len(salida["recomendaciones_siguientes"]) > 0)
            contenido = json.loads(out_json.read_text(encoding="utf-8"))
            for m in cargar_json(self.results)["modulos_resultados"]:
                self.assertFalse(m["usa_microsoft_real"])
                self.assertFalse(m["usa_microsoft_graph_real"])
                self.assertFalse(m["usa_oauth_real"])
                self.assertFalse(m["usa_api_externa"])
                self.assertFalse(m["usa_azure"])
                self.assertFalse(m["usa_ia_real"])
                self.assertFalse(m["usa_datos_reales"])
            self.assertIn("limites_declarados", contenido)


if __name__ == "__main__":
    unittest.main()
