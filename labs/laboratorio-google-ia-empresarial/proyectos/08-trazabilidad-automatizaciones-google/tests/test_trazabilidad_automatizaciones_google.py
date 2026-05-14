import json
import sys
import tempfile
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.trazabilidad_automatizaciones_google import cargar_json, generar_md, procesar, resumen, validar


class TestTrazabilidadAutomatizacionesGoogle(unittest.TestCase):
    def setUp(self):
        self.aut = BASE_DIR / "datos_ejemplo" / "automatizaciones_google_simuladas.json"
        self.cfg = BASE_DIR / "datos_ejemplo" / "configuracion_trazabilidad_automatizaciones.json"

    def test_existencia_archivos(self):
        self.assertTrue(self.aut.exists())
        self.assertTrue(self.cfg.exists())

    def test_carga_validacion(self):
        d = cargar_json(self.aut)
        c = cargar_json(self.cfg)
        validar(d["automatizaciones"], c)

    def test_trazabilidad_y_salidas(self):
        d = cargar_json(self.aut)
        c = cargar_json(self.cfg)
        with tempfile.TemporaryDirectory() as tmp:
            t = Path(tmp)
            r = procesar(d, c, t / "reg")
            self.assertTrue(all(x["id_traza"] for x in r))
            self.assertTrue(all(x["hash_simulado"] for x in r))
            self.assertTrue(any(x["requiere_revision"] for x in r))
            self.assertTrue(any(not x["trazabilidad_suficiente"] for x in r))
            self.assertTrue(all(Path(x["registro_generado"]).exists() for x in r))
            for x in r:
                self.assertFalse(x["usa_google_real"])
                self.assertFalse(x["usa_oauth_real"])
                self.assertFalse(x["usa_api_externa"])
                self.assertFalse(x["usa_cloud"])
                self.assertFalse(x["usa_ia_real"])
            s = resumen(r, c)
            j = t / "out.json"
            m = t / "out.md"
            j.write_text(json.dumps(s, ensure_ascii=False, indent=2), encoding="utf-8")
            generar_md(s, m)
            self.assertTrue(j.exists())
            self.assertTrue(m.exists())


if __name__ == "__main__":
    unittest.main()
