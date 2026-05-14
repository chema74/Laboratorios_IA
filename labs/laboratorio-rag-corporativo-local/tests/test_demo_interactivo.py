import json
import tempfile
import unittest
from pathlib import Path

from scripts.servidor_demo_interactivo import (
    CONSULTAS_EJEMPLO,
    _render_page,
    ejecutar_consulta_interactiva,
    ejecutar_self_test,
    guardar_evidencia_interactiva,
)


class TestDemoInteractivoRag(unittest.TestCase):
    def test_analisis_interactivo_fallback(self):
        r = ejecutar_consulta_interactiva(
            CONSULTAS_EJEMPLO["cumplimiento"],
            usar_groq=False,
            forzar_fallback_local=True,
        )
        self.assertEqual(r["proveedor"], "fallback_local")
        self.assertIn("fallback", r["ruta_ejecucion"])

    def test_generacion_evidencias(self):
        r = ejecutar_consulta_interactiva(
            CONSULTAS_EJEMPLO["operaciones"],
            usar_groq=False,
            forzar_fallback_local=True,
        )
        with tempfile.TemporaryDirectory() as tmp:
            rutas = guardar_evidencia_interactiva(r, carpeta=Path(tmp))
            self.assertTrue(rutas["json"].exists())
            self.assertTrue(rutas["markdown"].exists())

            payload = json.loads(rutas["json"].read_text(encoding="utf-8"))
            self.assertIn("consulta", payload)
            self.assertIn("fragmentos_recuperados", payload)
            self.assertIn("proveedor", payload)

            md = rutas["markdown"].read_text(encoding="utf-8")
            self.assertIn("Creative Commons CC BY-SA 4.0 International", md)
            self.assertIn("Txema Ríos", md)

    def test_self_test(self):
        ejecutar_self_test()

    def test_evidencias_aceptan_resumen_y_listas_como_dict(self):
        resultado = {
            "fecha": "2026-05-13T00:00:00+00:00",
            "consulta": "consulta demo",
            "rag": {
                "fragmentos": [
                    {"doc_id": "DOC-1", "titulo": "Documento A", "contenido": {"texto": "Contenido dict"}},
                    {"doc_id": "DOC-2", "titulo": "Documento B", "contenido": "Contenido texto"},
                ]
            },
            "analisis_llm": {
                "respuesta": {
                    "resumen": {"bloque": "Resumen estructurado"},
                    "riesgos": [{"id": "R1"}],
                    "recomendaciones": [{"id": "C1"}],
                }
            },
            "proveedor": "fallback_local",
            "modelo": "local-demo",
            "ruta_ejecucion": "fallback_forzado",
            "motivo_fallback": "prueba",
        }
        with tempfile.TemporaryDirectory() as tmp:
            rutas = guardar_evidencia_interactiva(resultado, carpeta=Path(tmp))
            md = rutas["markdown"].read_text(encoding="utf-8")
            self.assertIn("{\"bloque\": \"Resumen estructurado\"}", md)
            self.assertIn("{\"id\": \"R1\"}", md)
            self.assertIn("{\"id\": \"C1\"}", md)

    def test_html_contiene_bloques_clave(self):
        html = _render_page()
        self.assertIn("Laboratorio RAG corporativo local — Demo interactiva V2.1", html)
        self.assertIn("Escenarios predefinidos", html)
        self.assertIn("Historial local de consultas", html)
        self.assertIn("Fragmentos recuperados", html)
        self.assertIn("bloque-trazabilidad", html)
        self.assertIn("Evidencias generadas", html)
        self.assertIn("Qué demuestra esta demo", html)
        self.assertIn("Preparando consulta…", html)

    def test_render_fragmentos_dict_no_rompe(self):
        resultado = {
            "fecha": "2026-05-13T00:00:00+00:00",
            "consulta": "consulta demo",
            "rag": {
                "fragmentos": [
                    {"titulo": "Doc A", "referencia": "REF-1", "puntuacion": 0.98, "contenido": {"texto": "Bloque en dict"}},
                    {"doc_id": "DOC-2", "fragmento": ["línea", "dos"]},
                ]
            },
            "analisis_llm": {"respuesta": {"resumen": "OK", "riesgos": [], "recomendaciones": []}},
            "proveedor": "fallback_local",
            "modelo": "local-demo",
            "ruta_ejecucion": "fallback_forzado",
            "motivo_fallback": "prueba",
            "evidencias": {"json": "x.json", "markdown": "x.md"},
        }
        html = _render_page(resultado=resultado)
        self.assertIn("Doc A", html)
        self.assertIn("REF-1", html)
        self.assertIn("Score: 0.98", html)
        self.assertIn("Bloque en dict", html)
        self.assertIn("[&quot;línea&quot;, &quot;dos&quot;]", html)


if __name__ == "__main__":
    unittest.main()
