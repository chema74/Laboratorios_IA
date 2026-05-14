import json
import sys
import tempfile
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.simulador_calendar_tareas import cargar_json, generar_md, procesar, resumen_global, validar_elementos


class TestSimuladorCalendarTareas(unittest.TestCase):
    def setUp(self):
        self.events = BASE_DIR / "datos_ejemplo" / "eventos_tareas_sinteticos.json"
        self.config = BASE_DIR / "datos_ejemplo" / "configuracion_calendar_tareas.json"

    def test_existencia_archivos(self):
        self.assertTrue(self.events.exists())
        self.assertTrue(self.config.exists())

    def test_carga_validacion(self):
        d = cargar_json(self.events)
        c = cargar_json(self.config)
        self.assertIn("elementos", d)
        validar_elementos(d["elementos"], c)

    def test_procesamiento_salidas(self):
        d = cargar_json(self.events)
        c = cargar_json(self.config)
        with tempfile.TemporaryDirectory() as tmp:
            t = Path(tmp)
            resultados = procesar(d, c, t / "cal")
            self.assertTrue(any(x["tipo_elemento"] == "evento" for x in resultados))
            self.assertTrue(any(x["tipo_elemento"] == "tarea" for x in resultados))
            self.assertTrue(any(x["requiere_recordatorio"] for x in resultados))
            self.assertTrue(any(x["requiere_replanificacion"] for x in resultados))
            self.assertTrue(all(Path(x["registro_generado"]).exists() for x in resultados))
            for x in resultados:
                self.assertFalse(x["usa_calendar_real"])
                self.assertFalse(x["usa_oauth_real"])
                self.assertFalse(x["usa_api_externa"])
                self.assertFalse(x["usa_cloud"])
                self.assertFalse(x["usa_ia_real"])
            out = resumen_global(resultados, c)
            j = t / "out.json"
            m = t / "out.md"
            j.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
            generar_md(out, m)
            self.assertTrue(j.exists())
            self.assertTrue(m.exists())


if __name__ == "__main__":
    unittest.main()
