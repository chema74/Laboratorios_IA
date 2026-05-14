import sys
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.simulador_gmail_ia import (
    cargar_json,
    construir_resultado_global,
    procesar_correos,
    validar_correos,
)


class TestSimuladorGmailIA(unittest.TestCase):
    def setUp(self):
        self.base = BASE_DIR
        self.ruta_emails = self.base / "datos_ejemplo" / "correos_empresariales_sinteticos.json"
        self.ruta_config = self.base / "datos_ejemplo" / "configuracion_gmail_simulado.json"
        self.mailbox = self.base / "bandeja_simulada"

    def test_existen_archivos_de_datos(self):
        self.assertTrue(self.ruta_emails.exists())
        self.assertTrue(self.ruta_config.exists())

    def test_carga_y_validacion(self):
        data = cargar_json(self.ruta_emails)
        cfg = cargar_json(self.ruta_config)
        self.assertIn("correos", data)
        self.assertIn("categorias_permitidas", cfg)
        validar_correos(data["correos"], cfg)

    def test_procesamiento_y_resumen(self):
        data = cargar_json(self.ruta_emails)
        cfg = cargar_json(self.ruta_config)
        resultados = procesar_correos(data, cfg, self.mailbox)
        self.assertGreaterEqual(len(resultados), 1)
        self.assertTrue(any(x["requiere_respuesta"] for x in resultados))
        self.assertTrue(any(x["requiere_tarea"] for x in resultados))
        self.assertTrue(all(x["respuesta_sugerida_simulada"] for x in resultados))
        self.assertTrue(all(Path(x["registro_generado"]).exists() for x in resultados))
        resumen = construir_resultado_global(resultados, cfg)
        self.assertIn("distribucion_categoria", resumen)
        self.assertIn("distribucion_prioridad", resumen)
        for item in resultados:
            self.assertFalse(item["usa_gmail_real"])
            self.assertFalse(item["usa_oauth_real"])
            self.assertFalse(item["usa_api_externa"])
            self.assertFalse(item["usa_cloud"])
            self.assertFalse(item["usa_ia_real"])


if __name__ == "__main__":
    unittest.main()
