import json
import sys
import tempfile
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.conector_gemini_fallback import (
    cargar_json,
    generar_md,
    procesar,
    resumen_global,
    validar_solicitudes,
    verificar_modo,
)


class TestConectorGeminiFallback(unittest.TestCase):
    def setUp(self):
        self.req = BASE_DIR / "datos_ejemplo" / "solicitudes_gemini_simuladas.json"
        self.cfg = BASE_DIR / "datos_ejemplo" / "configuracion_gemini_fallback.json"

    def test_existencia_archivos(self):
        self.assertTrue(self.req.exists())
        self.assertTrue(self.cfg.exists())

    def test_carga_y_modo(self):
        d = cargar_json(self.req)
        c = cargar_json(self.cfg)
        verificar_modo(c)
        validar_solicitudes(d["solicitudes"], c)

    def test_fallback_y_salidas(self):
        d = cargar_json(self.req)
        c = cargar_json(self.cfg)
        with tempfile.TemporaryDirectory() as tmp:
            t = Path(tmp)
            res = procesar(d, c, t / "resp")
            self.assertTrue(all(x["modo_ejecucion"] == "fallback-local" for x in res))
            self.assertTrue(all(x["respuesta_simulada"] for x in res))
            self.assertTrue(all("fallback_local::" in x["trazabilidad_fallback"] for x in res))
            self.assertTrue(all(Path(x["registro_generado"]).exists() for x in res))
            for x in res:
                self.assertFalse(x["usa_gemini_real"])
                self.assertFalse(x["usa_api_externa"])
                self.assertFalse(x["usa_cloud"])
                self.assertFalse(x["usa_ia_real"])
            out = resumen_global(res, c)
            j = t / "out.json"
            m = t / "out.md"
            j.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
            generar_md(out, m)
            self.assertTrue(j.exists())
            self.assertTrue(m.exists())


if __name__ == "__main__":
    unittest.main()
