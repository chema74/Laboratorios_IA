import json
import sys
import tempfile
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.trazabilidad_automatizaciones_microsoft import cargar_json, ejecutar, validar_automatizaciones


class TestTrazabilidadAutomatizacionesMicrosoft(unittest.TestCase):
    def setUp(self):
        self.base = BASE_DIR
        self.autos = self.base / "datos_ejemplo" / "automatizaciones_microsoft_simuladas.json"
        self.config = self.base / "datos_ejemplo" / "configuracion_trazabilidad_automatizaciones.json"

    def test_existen_archivos(self):
        self.assertTrue(self.autos.exists())
        self.assertTrue(self.config.exists())

    def test_carga_y_validacion(self):
        data = cargar_json(self.autos)
        cfg = cargar_json(self.config)
        self.assertIn("automatizaciones", data)
        self.assertIn("origenes_permitidos", cfg)
        validar_automatizaciones(data["automatizaciones"], cfg)

    def test_ejecucion_completa(self):
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            out_md = td_path / "informe.md"
            out_json = td_path / "resultado.json"
            reg_dir = td_path / "reg"
            salida = ejecutar(self.autos, self.config, out_md, out_json, reg_dir)
            self.assertTrue(out_md.exists())
            self.assertTrue(out_json.exists())
            resultados = salida["resultados"]
            self.assertGreater(len(resultados), 0)
            self.assertTrue(all(r["id_traza"].startswith("TRZ-") for r in resultados))
            self.assertTrue(all(len(r["hash_simulado"]) == 64 for r in resultados))
            self.assertTrue(any(r["requiere_revision"] for r in resultados))
            self.assertTrue(any(not r["trazabilidad_suficiente"] for r in resultados))
            for r in resultados:
                self.assertTrue(Path(r["registro_generado"]).exists())
                self.assertFalse(r["usa_microsoft_real"])
                self.assertFalse(r["usa_microsoft_graph_real"])
                self.assertFalse(r["usa_oauth_real"])
                self.assertFalse(r["usa_api_externa"])
                self.assertFalse(r["usa_azure"])
                self.assertFalse(r["usa_ia_real"])
            contenido = json.loads(out_json.read_text(encoding="utf-8"))
            self.assertEqual(contenido["metadata"]["total_automatizaciones"], len(resultados))


if __name__ == "__main__":
    unittest.main()
