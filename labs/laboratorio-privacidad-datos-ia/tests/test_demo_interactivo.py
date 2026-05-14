import json
import tempfile
import unittest
from pathlib import Path

from scripts.servidor_demo_interactivo import (
    CASOS_EJEMPLO,
    analizar_texto_interactivo,
    guardar_evidencias_interactivas,
)


class TestDemoInteractiva(unittest.TestCase):
    def test_minimizacion_texto_con_pii(self):
        texto = "Cliente NombreDemo Uno con email cliente.demo@empresa.local y telefono 612345678"
        r = analizar_texto_interactivo(texto_original=texto, usar_groq=False, forzar_fallback_local=True)
        self.assertIn("[EMAIL]", r["texto_minimizado"])
        self.assertIn("[TELEFONO]", r["texto_minimizado"])

    def test_analisis_interactivo_fallback(self):
        texto = CASOS_EJEMPLO["lead"]
        r = analizar_texto_interactivo(texto_original=texto, usar_groq=False, forzar_fallback_local=True)
        self.assertEqual(r["proveedor"], "fallback_local")
        self.assertIn("FORZAR_FALLBACK_LOCAL", r.get("motivo_fallback", ""))

    def test_generacion_evidencia_json_markdown(self):
        texto = CASOS_EJEMPLO["cliente"]
        r = analizar_texto_interactivo(texto_original=texto, usar_groq=False, forzar_fallback_local=True)

        with tempfile.TemporaryDirectory() as tmp:
            rutas = guardar_evidencias_interactivas(r, carpeta=Path(tmp))
            self.assertTrue(rutas["json"].exists())
            self.assertTrue(rutas["markdown"].exists())

            payload = json.loads(rutas["json"].read_text(encoding="utf-8"))
            self.assertIn("texto_original", payload)
            self.assertIn("texto_minimizado", payload)
            self.assertIn("proveedor", payload)

            md = rutas["markdown"].read_text(encoding="utf-8")
            self.assertIn("Creative Commons CC BY-SA 4.0 International", md)
            self.assertIn("Txema Ríos", md)


if __name__ == "__main__":
    unittest.main()
