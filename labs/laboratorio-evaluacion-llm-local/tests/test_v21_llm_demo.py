import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from servicios.evaluacion_llm_v21 import evaluar_respuesta_llm, guardar_evidencia_json

BASE = Path(__file__).resolve().parents[1]


def cargar_servidor():
    ruta = BASE / "scripts" / "servidor_demo_interactivo.py"
    spec = importlib.util.spec_from_file_location("servidor_demo_interactivo_test", ruta)
    modulo = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(modulo)
    return modulo


class FakeGroqOK:
    class chat:
        class completions:
            @staticmethod
            def create(**kwargs):
                contenido = {
                    "puntuaciones": {
                        "relevancia": 0.8,
                        "precision": 0.75,
                        "cobertura": 0.7,
                        "seguridad": 0.9,
                        "consistencia": 0.85,
                        "trazabilidad": 0.8,
                    },
                    "riesgos": ["riesgo_bajo"],
                    "recomendaciones": ["ampliar fuentes"],
                    "explicacion": "Evaluación mock Groq",
                }

                class M:
                    choices = [type("Choice", (), {"message": type("Msg", (), {"content": json.dumps(contenido)})()})]

                return M()


class FakeGroqFail:
    class chat:
        class completions:
            @staticmethod
            def create(**kwargs):
                raise RuntimeError("fallo simulado")


class TestV21LLM(unittest.TestCase):
    def setUp(self):
        self.kw = {
            "escenario": "prueba",
            "pregunta": "¿Cuál es el estado del piloto?",
            "contexto": "El piloto está validado según informe interno.",
            "respuesta_candidata": "Según el informe interno, el piloto está validado.",
            "criterios": ["relevancia", "precision", "cobertura", "seguridad", "consistencia", "trazabilidad"],
        }

    def test_fallback_sin_api_key(self):
        with patch.dict(os.environ, {"GROQ_API_KEY": ""}, clear=False):
            r = evaluar_respuesta_llm(**self.kw)
        self.assertEqual(r["proveedor"], "fallback_local")

    def test_groq_simulado_con_mock(self):
        with patch.dict(os.environ, {"GROQ_API_KEY": "fake", "GROQ_MODEL": "llama-3.1-8b-instant"}, clear=False):
            r = evaluar_respuesta_llm(**self.kw, groq_client_factory=lambda api_key: FakeGroqOK())
        self.assertEqual(r["proveedor"], "groq")

    def test_fallo_groq_con_fallback(self):
        with patch.dict(os.environ, {"GROQ_API_KEY": "fake"}, clear=False):
            r = evaluar_respuesta_llm(**self.kw, groq_client_factory=lambda api_key: FakeGroqFail())
        self.assertEqual(r["proveedor"], "fallback_local")

    def test_evaluacion_determinista_local(self):
        with patch.dict(os.environ, {"GROQ_API_KEY": ""}, clear=False):
            a = evaluar_respuesta_llm(**self.kw)
            b = evaluar_respuesta_llm(**self.kw)
        self.assertEqual(a["puntuaciones"], b["puntuaciones"])

    def test_generacion_evidencias_json(self):
        with tempfile.TemporaryDirectory() as td:
            out = guardar_evidencia_json({"ok": True}, Path(td) / "ev.json")
            self.assertTrue(out.exists())

    def test_get_root_contiene_selector_y_escenarios(self):
        s = cargar_servidor()
        html = s._handle_get_root()
        self.assertIn("<select name='escenario'>", html)
        self.assertIn("Respuesta correcta pero incompleta", html)
        self.assertIn("Respuesta RAG con contexto insuficiente", html)

    def test_post_cargar_rellena_campos(self):
        s = cargar_servidor()
        html = s._handle_post_cargar({"escenario": ["respuesta_correcta_incompleta"]})
        self.assertIn("Escenario cargado", html)
        self.assertIn("Resume la estrategia comercial para dirección.", html)
        self.assertIn("Objetivos: crecimiento B2B", html)
        self.assertIn("La estrategia prioriza crecimiento B2B", html)

    def test_post_evaluar_fallback_muestra_resultados(self):
        s = cargar_servidor()
        html = s._handle_post_evaluar({
            "escenario": ["respuesta_correcta_incompleta"],
            "pregunta": ["Resume la estrategia comercial para dirección."],
            "contexto_esperado": ["Objetivos: crecimiento B2B, mejora de margen y expansión regional. Riesgos: churn y presión competitiva."],
            "respuesta_candidata": ["La estrategia prioriza crecimiento B2B y mejora de margen."],
            "criterios": ["relevancia", "precision", "cobertura"],
            "forzar_fallback": ["1"],
        })
        for token in ["Puntuaciones", "Explicación", "Riesgos", "Recomendaciones", "Trazabilidad", "fallback_local"]:
            self.assertIn(token, html)

    def test_html_no_depende_de_js_para_cargar(self):
        s = cargar_servidor()
        html = s._handle_get_root()
        self.assertIn("<form method='POST' action='/cargar'>", html)
        self.assertIn("<form method='POST' action='/evaluar'>", html)

    def test_html_contiene_bloques_narrativos(self):
        s = cargar_servidor()
        html = s._handle_get_root()
        for token in [
            "Para qué sirve este laboratorio",
            "Qué demuestra técnicamente",
            "Cómo lo usaría una empresa",
            "Cómo interpretar las puntuaciones",
            "1. Caso a evaluar",
            "2. Evaluación generada",
            "3. Evidencias generadas",
        ]:
            self.assertIn(token, html)

    def test_demo_llm_groq_usa_esquema_nuevo_sin_keyerror_contexto(self):
        env = os.environ.copy()
        env["FORZAR_FALLBACK_LOCAL"] = "1"
        env["GROQ_API_KEY"] = ""
        cmd = [sys.executable, str(BASE / "scripts" / "demo_llm_groq.py")]
        p = subprocess.run(cmd, cwd=BASE, capture_output=True, text=True, check=False, env=env)
        self.assertEqual(p.returncode, 0)
        self.assertIn("Casos evaluados: 5", p.stdout)
        self.assertNotIn("KeyError: 'contexto'", p.stdout + p.stderr)

    def test_self_test_servidor(self):
        cmd = [sys.executable, str(BASE / "scripts" / "servidor_demo_interactivo.py"), "--self-test"]
        p = subprocess.run(cmd, cwd=BASE, capture_output=True, text=True, check=False)
        self.assertEqual(p.returncode, 0)
        self.assertIn("SELF_TEST_OK", p.stdout)


if __name__ == "__main__":
    unittest.main()
