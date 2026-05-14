from __future__ import annotations

import importlib.util
import json
import os
import unittest
from pathlib import Path


class TestEvidenciasV21(unittest.TestCase):
    def test_generacion_archivos(self):
        base = Path(__file__).resolve().parents[1]
        ruta = base / "scripts" / "generar_evidencias_v21.py"
        spec = importlib.util.spec_from_file_location("gen_v21", ruta)
        modulo = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(modulo)

        os.environ["OBSERVABILIDAD_MODO"] = "fallback_local"
        os.environ.pop("GROQ_API_KEY", None)
        rutas = modulo.generar_evidencias("uso_normal_controlado")
        self.assertTrue(rutas["json"].exists())
        self.assertTrue(rutas["md"].exists())
        self.assertTrue(rutas["html"].exists())

        data = json.loads(rutas["json"].read_text(encoding="utf-8"))
        self.assertIn("metricas_agregadas", data)
        self.assertIn(data["modo"], {"fallback_local", "groq"})
        self.assertIn("diagnostico_groq", data)
        self.assertIn("solicitado", data["diagnostico_groq"])


if __name__ == "__main__":
    unittest.main()
