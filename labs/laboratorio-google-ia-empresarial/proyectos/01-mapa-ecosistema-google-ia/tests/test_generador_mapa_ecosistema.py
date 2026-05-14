import json
import sys
import tempfile
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.generador_mapa_ecosistema import (
    cargar_json,
    clasificar_por_clave,
    generar_informe_markdown,
    generar_resultado,
    validar_componentes,
)


class TestGeneradorMapaEcosistema(unittest.TestCase):
    def setUp(self):
        self.base = BASE_DIR
        self.ecosystem = self.base / "datos_ejemplo" / "ecosistema_google_ia_sintetico.json"
        self.config = self.base / "datos_ejemplo" / "configuracion_mapa_google_ia.json"

    def test_existen_archivos_de_datos(self):
        self.assertTrue(self.ecosystem.exists())
        self.assertTrue(self.config.exists())

    def test_carga_y_validacion(self):
        eco = cargar_json(self.ecosystem)
        cfg = cargar_json(self.config)
        self.assertIn("componentes", eco)
        self.assertIn("categorias_permitidas", cfg)
        validar_componentes(eco["componentes"], cfg)
        self.assertGreaterEqual(len(eco["componentes"]), 8)

    def test_clasificacion_por_categoria_y_capa(self):
        eco = cargar_json(self.ecosystem)
        por_categoria = clasificar_por_clave(eco["componentes"], "categoria")
        por_capa = clasificar_por_clave(eco["componentes"], "capa_arquitectura")
        self.assertGreaterEqual(len(por_categoria.keys()), 3)
        self.assertGreaterEqual(len(por_capa.keys()), 3)

    def test_no_dependencias_reales_obligatorias(self):
        eco = cargar_json(self.ecosystem)
        for comp in eco["componentes"]:
            self.assertFalse(comp["dependencia_real_obligatoria"])
            self.assertFalse(comp["requiere_oauth_real"])
            self.assertFalse(comp["requiere_api_real"])
            self.assertFalse(comp["requiere_cloud"])
            self.assertTrue(comp["v1_local_simulada"])

    def test_generacion_json_y_markdown(self):
        eco = cargar_json(self.ecosystem)
        cfg = cargar_json(self.config)
        resultado = generar_resultado(eco, cfg)
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            ruta_md = tmp / "informe.md"
            ruta_json = tmp / "salida.json"
            ruta_json.write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8")
            generar_informe_markdown(resultado, ruta_md)
            self.assertTrue(ruta_md.exists())
            self.assertTrue(ruta_json.exists())
            self.assertIn("Límites de la V1 local", ruta_md.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
