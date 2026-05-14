import json
import sys
import tempfile
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.simulador_excel_ia import cargar_config, cargar_csv, ejecutar, validar_columnas


class TestSimuladorExcelIA(unittest.TestCase):
    def setUp(self):
        self.base = BASE_DIR
        self.csv_path = self.base / "datos_ejemplo" / "libro_excel_operativo_sintetico.csv"
        self.config_path = self.base / "datos_ejemplo" / "configuracion_excel_analitica.json"

    def test_existen_archivos_base(self):
        self.assertTrue(self.csv_path.exists())
        self.assertTrue(self.config_path.exists())

    def test_carga_csv_y_config(self):
        regs = cargar_csv(self.csv_path)
        cfg = cargar_config(self.config_path)
        self.assertGreater(len(regs), 0)
        self.assertIn("columnas_esperadas", cfg)

    def test_validacion_columnas(self):
        regs = cargar_csv(self.csv_path)
        cfg = cargar_config(self.config_path)
        validar_columnas(regs, cfg["columnas_esperadas"])

    def test_simulacion_completa(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            out_md = tmp / "informe.md"
            out_json = tmp / "resultado.json"
            wb_dir = tmp / "wb"
            resultado = ejecutar(self.csv_path, self.config_path, out_md, out_json, wb_dir)
            self.assertTrue(out_md.exists())
            self.assertTrue(out_json.exists())
            self.assertIn("indicadores_financieros_simulados", resultado)
            self.assertIn("distribuciones", resultado)
            self.assertIn("señales_analiticas_simuladas", resultado)
            self.assertTrue(Path(resultado["libro_enriquecido_generado"]).exists())
            self.assertGreaterEqual(len(resultado["registros_revision"]), 1)
            self.assertFalse(resultado["usa_excel_real"])
            self.assertFalse(resultado["usa_microsoft_graph_real"])
            self.assertFalse(resultado["usa_oauth_real"])
            self.assertFalse(resultado["usa_api_externa"])
            self.assertFalse(resultado["usa_azure"])
            self.assertFalse(resultado["usa_ia_real"])
            contenido = json.loads(out_json.read_text(encoding="utf-8"))
            self.assertIn("indicadores_operativos", contenido)


if __name__ == "__main__":
    unittest.main()
