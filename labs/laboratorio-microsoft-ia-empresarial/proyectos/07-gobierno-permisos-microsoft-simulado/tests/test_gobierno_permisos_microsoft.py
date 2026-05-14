import json
import sys
import tempfile
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.gobierno_permisos_microsoft import cargar_json, ejecutar, validar_permisos


class TestGobiernoPermisosMicrosoft(unittest.TestCase):
    def setUp(self):
        self.base = BASE_DIR
        self.permissions = self.base / "datos_ejemplo" / "permisos_microsoft_simulados.json"
        self.config = self.base / "datos_ejemplo" / "configuracion_gobierno_permisos.json"

    def test_existen_archivos(self):
        self.assertTrue(self.permissions.exists())
        self.assertTrue(self.config.exists())

    def test_carga_y_validacion(self):
        data = cargar_json(self.permissions)
        cfg = cargar_json(self.config)
        self.assertIn("permisos", data)
        self.assertIn("roles_permitidos", cfg)
        validar_permisos(data["permisos"], cfg)

    def test_ejecucion_completa(self):
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            out_md = td_path / "informe.md"
            out_json = td_path / "resultado.json"
            reg_dir = td_path / "reg"
            salida = ejecutar(self.permissions, self.config, out_md, out_json, reg_dir)
            self.assertTrue(out_md.exists())
            self.assertTrue(out_json.exists())
            self.assertIn("resumen_por_decision", salida)
            resultados = salida["resultados"]
            self.assertGreater(len(resultados), 0)
            self.assertTrue(any(r["decision_gobierno"] in {"reducir", "revocar"} for r in resultados))
            self.assertTrue(any(r["decision_gobierno"] == "revisar" for r in resultados))
            for r in resultados:
                self.assertTrue(Path(r["registro_generado"]).exists())
                self.assertFalse(r["usa_microsoft_real"])
                self.assertFalse(r["usa_microsoft_graph_real"])
                self.assertFalse(r["usa_oauth_real"])
                self.assertFalse(r["usa_api_externa"])
                self.assertFalse(r["usa_azure"])
                self.assertFalse(r["usa_ia_real"])
            contenido = json.loads(out_json.read_text(encoding="utf-8"))
            self.assertEqual(contenido["metadata"]["total_permisos"], len(resultados))


if __name__ == "__main__":
    unittest.main()
