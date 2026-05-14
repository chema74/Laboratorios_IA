from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

BASE = Path(__file__).resolve().parents[1]
SRC = BASE / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from observabilidad_costes_ia.integracion_groq import GroqError, analizar_con_groq


class _RespuestaFake:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        payload = {
            "choices": [
                {
                    "message": {
                        "content": json.dumps(
                            {
                                "resumen_ejecutivo": "ok",
                                "riesgos_detectados": ["r1"],
                                "recomendaciones_optimizacion_coste": ["c1"],
                                "recomendaciones_operacion": ["o1"],
                                "alertas_gobernanza_uso_responsable": ["g1"],
                            },
                            ensure_ascii=False,
                        )
                    }
                }
            ]
        }
        return json.dumps(payload, ensure_ascii=False).encode("utf-8")


class TestGroqMockV21(unittest.TestCase):
    @patch("observabilidad_costes_ia.integracion_groq.request.urlopen", return_value=_RespuestaFake())
    def test_integracion_groq_mock(self, mock_urlopen):
        os.environ["GROQ_API_KEY"] = "dummy"
        os.environ["GROQ_MODEL"] = "modelo-test"
        r = analizar_con_groq({"total_eventos": 1})
        self.assertEqual(r["modo"], "groq")
        self.assertEqual(r["modelo_groq"], "modelo-test")
        req = mock_urlopen.call_args.args[0]
        headers = {k.lower(): v for k, v in req.header_items()}
        self.assertEqual(headers["accept"], "application/json")
        self.assertEqual(headers["user-agent"], "portfolio-observabilidad-costes-ia/2.1 Python-urllib")

    def test_falla_sin_clave(self):
        os.environ.pop("GROQ_API_KEY", None)
        with self.assertRaises(GroqError) as ctx:
            analizar_con_groq({"total_eventos": 1})
        self.assertEqual(ctx.exception.categoria, "falta_clave")


if __name__ == "__main__":
    unittest.main()
