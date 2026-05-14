import json
import os
import unittest
from unittest.mock import patch

from servicios.analisis_llm import analizar_rag_llm


class _Resp:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        contenido = {
            "choices": [
                {
                    "message": {
                        "content": json.dumps(
                            {
                                "resumen": "OK RAG",
                                "riesgos": ["R1"],
                                "recomendaciones": ["C1"],
                            },
                            ensure_ascii=False,
                        )
                    }
                }
            ]
        }
        return json.dumps(contenido).encode("utf-8")


def _fragmentos_base():
    return [
        {
            "doc_id": "DOC-003",
            "titulo": "Protocolo soporte",
            "contenido": "SLA crítico 30 minutos.",
            "puntuacion": 0.9,
        }
    ]


class TestAnalisisLLMRag(unittest.TestCase):
    def test_fallback_sin_api_key(self):
        with patch.dict(os.environ, {}, clear=True):
            r = analizar_rag_llm(
                "consulta demo",
                _fragmentos_base(),
                api_key=None,
                cargar_env=False,
                entorno={},
            )
        self.assertEqual(r["proveedor"], "fallback_local")
        self.assertIn("GROQ_API_KEY", r["motivo_fallback"])

    def test_groq_simulado_ok(self):
        def opener_ok(_req, timeout=20):
            return _Resp()

        with patch.dict(os.environ, {}, clear=True):
            r = analizar_rag_llm(
                "consulta demo",
                _fragmentos_base(),
                api_key="dummy",
                opener=opener_ok,
                cargar_env=False,
                entorno={"GROQ_MODEL": "modelo-test"},
            )
        self.assertEqual(r["proveedor"], "groq")
        self.assertEqual(r["respuesta"]["resumen"], "OK RAG")

    def test_fallback_si_falla_groq(self):
        def opener_fail(_req, timeout=20):
            raise TimeoutError("timeout simulado")

        with patch.dict(os.environ, {}, clear=True):
            r = analizar_rag_llm(
                "consulta demo",
                _fragmentos_base(),
                api_key="dummy",
                opener=opener_fail,
                cargar_env=False,
                entorno={},
            )
        self.assertEqual(r["proveedor"], "fallback_local")
        self.assertIn("TimeoutError", r["motivo_fallback"])

    def test_prompt_normaliza_fragmentos_mixtos(self):
        capturado = {}

        def opener_ok(req, timeout=20):
            capturado["body"] = json.loads(req.data.decode("utf-8"))
            return _Resp()

        fragmentos = [
            "Texto plano de política interna.",
            {"titulo": "Norma A", "contenido": {"detalle": "Control trimestral"}},
            {"referencia": "REF-77"},
            {"sin_campos": 123, "lista": [1, 2]},
        ]

        with patch.dict(os.environ, {}, clear=True):
            r = analizar_rag_llm(
                "consulta demo",
                fragmentos,
                api_key="dummy",
                opener=opener_ok,
                cargar_env=False,
                entorno={"GROQ_MODEL": "modelo-test"},
            )

        self.assertEqual(r["proveedor"], "groq")
        prompt_usuario = capturado["body"]["messages"][1]["content"]
        self.assertIn("[1] Texto plano de política interna.", prompt_usuario)
        self.assertIn("[2] {\"detalle\": \"Control trimestral\"}", prompt_usuario)
        self.assertIn("[3] REF-77", prompt_usuario)
        self.assertIn("[4] {\"sin_campos\": 123, \"lista\": [1, 2]}", prompt_usuario)


if __name__ == "__main__":
    unittest.main()
