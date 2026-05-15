import json
import sys
import tempfile
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.simulador_sheets_ia import (
    calcular_distribuciones,
    calcular_indicadores,
    cargar_config,
    cargar_csv,
    construir_resultado,
    detectar_senales,
    generar_informe_markdown,
    guardar_hoja_enriquecida,
    validar_columnas,
)


class TestSimuladorSheetsIA(unittest.TestCase):
    def setUp(self):
        self.base = BASE_DIR
        self.sheet = self.base / "datos_ejemplo" / "hoja_operativa_sintetica.csv"
        self.config = self.base / "datos_ejemplo" / "configuracion_sheets_analitica.json"

    def test_existen_archivos(self):
        self.assertTrue(self.sheet.exists())
        self.assertTrue(self.config.exists())

    def test_carga_validacion_metricas(self):
        registros = cargar_csv(self.sheet)
        cfg = cargar_config(self.config)
        validar_columnas(registros, cfg["columnas_esperadas"])
        indicadores = calcular_indicadores(registros)
        distribuciones = calcular_distribuciones(registros)
        senales = detectar_senales(registros, cfg)
        self.assertGreater(indicadores["importe_total_simulado"], 0)
        self.assertIn("por_area_negocio", distribuciones)
        self.assertTrue(isinstance(senales, list))

    def test_salidas_archivos(self):
        registros = cargar_csv(self.sheet)
        cfg = cargar_config(self.config)
        with tempfile.TemporaryDirectory() as tmp:
            tmp_dir = Path(tmp)
            hoja = guardar_hoja_enriquecida(registros, tmp_dir / "sheets")
            resultado = construir_resultado(registros, cfg, hoja)
            out_json = tmp_dir / "resultado.json"
            out_md = tmp_dir / "informe.md"
            out_json.write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8")
            generar_informe_markdown(resultado, out_md)
            self.assertTrue(Path(hoja).exists())
            self.assertTrue(out_json.exists())
            self.assertTrue(out_md.exists())
            self.assertFalse(resultado["usa_sheets_real"])
            self.assertFalse(resultado["usa_oauth_real"])
            self.assertFalse(resultado["usa_api_externa"])
            self.assertFalse(resultado["usa_cloud"])
            self.assertFalse(resultado["usa_ia_real"])


if __name__ == "__main__":
    unittest.main()
