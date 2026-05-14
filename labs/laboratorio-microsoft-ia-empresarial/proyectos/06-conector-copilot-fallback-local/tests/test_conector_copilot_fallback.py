import json
import sys
import tempfile
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.conector_copilot_fallback import cargar_json, ejecutar, validar_config, validar_solicitudes


class TestConectorCopilotFallback(unittest.TestCase):
    def setUp(self):
        self.base = BASE_DIR
        self.requests = self.base / "datos_ejemplo" / "solicitudes_copilot_simuladas.json"
        self.config = self.base / "datos_ejemplo" / "configuracion_copilot_fallback.json"

    def test_existen_archivos(self):
        self.assertTrue(self.requests.exists())
        self.assertTrue(self.config.exists())

    def test_carga_y_validacion(self):
        data = cargar_json(self.requests)
        cfg = cargar_json(self.config)
        self.assertIn("solicitudes", data)
        self.assertIn("modo_v1", cfg)
        validar_config(cfg)
        validar_solicitudes(data["solicitudes"], cfg)

    def test_modo_fallback_activo(self):
        cfg = cargar_json(self.config)
        self.assertEqual(cfg["modo_v1"], "fallback-local")
        self.assertFalse(cfg["permitir_copilot_real"])
        self.assertFalse(cfg["permitir_microsoft_graph_real"])

    def test_ejecucion_completa(self):
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            out_md = td_path / "informe.md"
            out_json = td_path / "resultado.json"
            res_dir = td_path / "respuestas"
            salida = ejecutar(self.requests, self.config, out_md, out_json, res_dir)
            self.assertTrue(out_md.exists())
            self.assertTrue(out_json.exists())
            self.assertIn("resumen_por_tipo_solicitud", salida)
            self.assertIn("resumen_por_origen", salida)
            resultados = salida["resultados"]
            self.assertGreater(len(resultados), 0)
            for r in resultados:
                self.assertEqual(r["modo_ejecucion"], "fallback-local")
                self.assertTrue(r["respuesta_simulada"])
                self.assertIn("fallback-local", r["trazabilidad_fallback"])
                self.assertTrue(Path(r["registro_generado"]).exists())
                self.assertFalse(r["usa_copilot_real"])
                self.assertFalse(r["usa_microsoft_graph_real"])
                self.assertFalse(r["usa_api_externa"])
                self.assertFalse(r["usa_azure"])
                self.assertFalse(r["usa_ia_real"])
            contenido = json.loads(out_json.read_text(encoding="utf-8"))
            self.assertEqual(contenido["metadata"]["modo_v1"], "fallback-local")


if __name__ == "__main__":
    unittest.main()
