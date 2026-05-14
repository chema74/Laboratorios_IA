import json
import sys
import tempfile
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.gobierno_permisos_google import cargar_json, generar_md, procesar, resumen, validar


class TestGobiernoPermisosGoogle(unittest.TestCase):
    def setUp(self):
        self.permissions = BASE_DIR / "datos_ejemplo" / "permisos_google_simulados.json"
        self.config = BASE_DIR / "datos_ejemplo" / "configuracion_gobierno_permisos.json"

    def test_existencia_archivos(self):
        self.assertTrue(self.permissions.exists())
        self.assertTrue(self.config.exists())

    def test_carga_validacion(self):
        d = cargar_json(self.permissions)
        c = cargar_json(self.config)
        validar(d["permisos"], c)

    def test_procesamiento(self):
        d = cargar_json(self.permissions)
        c = cargar_json(self.config)
        with tempfile.TemporaryDirectory() as tmp:
            t = Path(tmp)
            r = procesar(d, c, t / "reg")
            self.assertTrue(any(x["decision_gobierno"] in {"reducir", "revocar"} for x in r))
            self.assertTrue(all(x["decision_gobierno"] in {"mantener", "revisar", "reducir", "revocar"} for x in r))
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
