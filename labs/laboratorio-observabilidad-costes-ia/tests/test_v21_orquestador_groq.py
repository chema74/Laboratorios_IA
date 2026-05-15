from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

BASE = Path(__file__).resolve().parents[1]
SRC = BASE / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from observabilidad_costes_ia.escenarios import obtener_escenario
from observabilidad_costes_ia.integracion_groq import GroqError
from observabilidad_costes_ia.motor import analizar_eventos
from observabilidad_costes_ia.orquestador import generar_analisis_ejecutivo


class TestOrquestadorGroqV21(unittest.TestCase):
    def setUp(self):
        self.metrica = analizar_eventos(obtener_escenario("uso_normal_controlado"))
        os.environ.pop("GROQ_API_KEY", None)
        os.environ.pop("OBSERVABILIDAD_MODO", None)

    def test_fallback_forzado_diagnostico(self):
        os.environ["OBSERVABILIDAD_MODO"] = "fallback_local"
        r = generar_analisis_ejecutivo(self.metrica)
        self.assertEqual(r["modo"], "fallback_local")
        self.assertIn("diagnostico_groq", r)
        self.assertFalse(r["diagnostico_groq"]["solicitado"])
        self.assertEqual(r["diagnostico_groq"]["categoria"], "modo_fallback_forzado")

    def test_groq_sin_clave(self):
        os.environ["OBSERVABILIDAD_MODO"] = "groq"
        r = generar_analisis_ejecutivo(self.metrica)
        self.assertEqual(r["modo"], "fallback_local")
        self.assertTrue(r["diagnostico_groq"]["solicitado"])
        self.assertEqual(r["diagnostico_groq"]["estado"], "fallo")
        self.assertEqual(r["diagnostico_groq"]["categoria"], "falta_clave")

    @patch("observabilidad_costes_ia.orquestador.analizar_con_groq")
    def test_groq_mock_ok(self, mock_groq):
        os.environ["OBSERVABILIDAD_MODO"] = "groq"
        os.environ["GROQ_API_KEY"] = "dummy"
        mock_groq.return_value = {
            "modo": "groq",
            "resumen_ejecutivo": "ok",
            "riesgos_detectados": ["r1"],
            "recomendaciones_optimizacion_coste": ["c1"],
            "recomendaciones_operacion": ["o1"],
            "alertas_gobernanza_uso_responsable": ["g1"],
            "http_status_groq": 200,
            "modelo_groq": "modelo-test",
        }
        r = generar_analisis_ejecutivo(self.metrica)
        self.assertEqual(r["modo"], "groq")
        self.assertEqual(r["diagnostico_groq"]["estado"], "ok")
        self.assertEqual(r["diagnostico_groq"]["categoria"], "groq_ok")

    @patch("observabilidad_costes_ia.orquestador.analizar_con_groq")
    def test_groq_mock_fallo(self, mock_groq):
        os.environ["OBSERVABILIDAD_MODO"] = "groq"
        os.environ["GROQ_API_KEY"] = "dummy"
        mock_groq.side_effect = GroqError(
            categoria="timeout_red",
            mensaje_seguro="Timeout de red al invocar Groq.",
            http_status=None,
            modelo="modelo-test",
        )
        r = generar_analisis_ejecutivo(self.metrica)
        self.assertEqual(r["modo"], "fallback_local")
        self.assertEqual(r["diagnostico_groq"]["estado"], "fallo")
        self.assertEqual(r["diagnostico_groq"]["categoria"], "timeout_red")


if __name__ == "__main__":
    unittest.main()
