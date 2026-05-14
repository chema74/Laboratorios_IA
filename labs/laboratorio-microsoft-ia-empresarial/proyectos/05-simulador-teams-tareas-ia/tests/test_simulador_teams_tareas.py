import json
import sys
import tempfile
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.simulador_teams_tareas import cargar_json, ejecutar, validar_elementos


class TestSimuladorTeamsTareas(unittest.TestCase):
    def setUp(self):
        self.base = BASE_DIR
        self.items = self.base / "datos_ejemplo" / "conversaciones_tareas_teams_sinteticas.json"
        self.config = self.base / "datos_ejemplo" / "configuracion_teams_tareas.json"

    def test_existen_archivos(self):
        self.assertTrue(self.items.exists())
        self.assertTrue(self.config.exists())

    def test_carga_y_validacion(self):
        data = cargar_json(self.items)
        cfg = cargar_json(self.config)
        self.assertIn("elementos", data)
        self.assertIn("tipos_elemento_permitidos", cfg)
        validar_elementos(data["elementos"], cfg)

    def test_detecta_tipos(self):
        data = cargar_json(self.items)
        tipos = {e["tipo_elemento"] for e in data["elementos"]}
        self.assertTrue({"mensaje", "reunion", "tarea"}.issubset(tipos))

    def test_simulacion_completa(self):
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            out_md = td_path / "informe.md"
            out_json = td_path / "resultado.json"
            teams_dir = td_path / "teams"
            salida = ejecutar(self.items, self.config, out_md, out_json, teams_dir)
            self.assertTrue(out_md.exists())
            self.assertTrue(out_json.exists())
            self.assertIn("resumen_por_canal", salida)
            self.assertIn("resumen_por_tipo", salida)
            resultados = salida["resultados"]
            self.assertGreater(len(resultados), 0)
            self.assertTrue(any(r["resumen_simulado"] != "No aplica" for r in resultados))
            self.assertTrue(any(r["tarea_recomendada_simulada"] != "No aplica" for r in resultados))
            self.assertTrue(any(r["seguimiento_recomendado_simulado"] != "No aplica" for r in resultados))
            for r in resultados:
                self.assertTrue(Path(r["registro_generado"]).exists())
                self.assertFalse(r["usa_teams_real"])
                self.assertFalse(r["usa_planner_real"])
                self.assertFalse(r["usa_todo_real"])
                self.assertFalse(r["usa_microsoft_graph_real"])
                self.assertFalse(r["usa_oauth_real"])
                self.assertFalse(r["usa_api_externa"])
                self.assertFalse(r["usa_azure"])
                self.assertFalse(r["usa_ia_real"])
            contenido = json.loads(out_json.read_text(encoding="utf-8"))
            self.assertEqual(contenido["metadata"]["total_elementos"], len(resultados))


if __name__ == "__main__":
    unittest.main()
