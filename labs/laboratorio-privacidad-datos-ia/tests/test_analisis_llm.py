import json
import os
import unittest
from unittest.mock import patch

from servicios.analisis_llm import analizar_privacidad_llm


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
                                "resumen": "OK",
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


def _motor_base():
    return {
        "analisis_casos": [{"detecciones": [{"severidad": "alta"}]}],
        "evaluacion_exposicion": {"nivel_riesgo": "alto", "puntuacion": 8},
        "validacion_salidas": [{"estado": "bloquear"}],
    }


class TestAnalisisLLM(unittest.TestCase):
    def test_fallback_sin_api_key(self):
        with patch.dict(os.environ, {}, clear=True):
            r = analizar_privacidad_llm(_motor_base(), api_key=None, cargar_env=False, entorno={})
        self.assertEqual(r["proveedor"], "fallback_local")
        self.assertIn("motivo_fallback", r)

    def test_groq_simulado_ok(self):
        def opener_ok(_req, timeout=20):
            return _Resp()

        with patch.dict(os.environ, {}, clear=True):
            r = analizar_privacidad_llm(
                _motor_base(),
                api_key="dummy",
                opener=opener_ok,
                cargar_env=False,
                entorno={"GROQ_MODEL": "modelo-test"},
            )
        self.assertEqual(r["proveedor"], "groq")
        self.assertEqual(r["respuesta"]["resumen"], "OK")

    def test_fallback_si_falla_groq(self):
        def opener_fail(_req, timeout=20):
            raise TimeoutError("timeout simulado")

        with patch.dict(os.environ, {}, clear=True):
            r = analizar_privacidad_llm(
                _motor_base(),
                api_key="dummy",
                opener=opener_fail,
                cargar_env=False,
                entorno={},
            )
        self.assertEqual(r["proveedor"], "fallback_local")
        self.assertIn("TimeoutError", r["motivo_fallback"])

    def test_fallback_forzado_por_variable(self):
        with patch.dict(os.environ, {}, clear=True):
            r = analizar_privacidad_llm(
                _motor_base(),
                api_key="dummy",
                cargar_env=False,
                entorno={"FORZAR_FALLBACK_LOCAL": "1"},
            )
        self.assertEqual(r["proveedor"], "fallback_local")
        self.assertIn("FORZAR_FALLBACK_LOCAL", r["motivo_fallback"])


if __name__ == "__main__":
    unittest.main()
