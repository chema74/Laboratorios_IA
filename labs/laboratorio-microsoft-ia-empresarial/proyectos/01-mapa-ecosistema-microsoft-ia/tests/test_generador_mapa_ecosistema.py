import json
import sys
import tempfile
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.generador_mapa_ecosistema import agrupar_por_clave, cargar_json, ejecutar, validar_componentes


class TestGeneradorMapaEcosistema(unittest.TestCase):
    def setUp(self):
        self.base = Path(__file__).resolve().parents[1]
        self.ecosystem_path = self.base / "datos_ejemplo" / "ecosistema_microsoft_ia_sintetico.json"
        self.config_path = self.base / "datos_ejemplo" / "configuracion_mapa_microsoft_ia.json"

    def test_existen_archivos_base(self):
        self.assertTrue(self.ecosystem_path.exists())
        self.assertTrue(self.config_path.exists())

    def test_carga_ecosistema_y_config(self):
        ecosystem = cargar_json(self.ecosystem_path)
        config = cargar_json(self.config_path)
        self.assertIn("componentes", ecosystem)
        self.assertIn("categorias_permitidas", config)

    def test_validacion_componentes(self):
        ecosystem = cargar_json(self.ecosystem_path)
        config = cargar_json(self.config_path)
        componentes = ecosystem["componentes"]
        self.assertGreaterEqual(len(componentes), 8)
        validar_componentes(componentes, config)

    def test_clasificacion_por_categoria_y_capa(self):
        ecosystem = cargar_json(self.ecosystem_path)
        componentes = ecosystem["componentes"]
        por_categoria = agrupar_por_clave(componentes, "categoria")
        por_capa = agrupar_por_clave(componentes, "capa_arquitectura")
        self.assertGreaterEqual(len(por_categoria), 4)
        self.assertGreaterEqual(len(por_capa), 4)

    def test_no_dependencias_reales_obligatorias(self):
        ecosystem = cargar_json(self.ecosystem_path)
        for comp in ecosystem["componentes"]:
            self.assertFalse(comp["dependencia_real_obligatoria"])
            self.assertFalse(comp["requiere_oauth_real"])
            self.assertFalse(comp["requiere_api_real"])
            self.assertFalse(comp["requiere_azure"])

    def test_genera_informe_y_json_salida(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            out_md = tmp / "informe.md"
            out_json = tmp / "salida.json"
            resultado = ejecutar(self.ecosystem_path, self.config_path, out_md, out_json)
            self.assertTrue(out_md.exists())
            self.assertTrue(out_json.exists())
            self.assertIn("resumen_por_categoria", resultado)

            contenido = json.loads(out_json.read_text(encoding="utf-8"))
            controles = contenido.get("controles_v1", {})
            self.assertFalse(controles.get("requiere_oauth_real", True))
            self.assertFalse(controles.get("requiere_api_real", True))
            self.assertFalse(controles.get("requiere_azure", True))
            self.assertFalse(controles.get("usa_ia_real", True))
            self.assertFalse(controles.get("usa_datos_reales", True))


if __name__ == "__main__":
    unittest.main()
