from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


class TestDashboardV21(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        base = Path(__file__).resolve().parents[1]
        ruta = base / "scripts" / "dashboard_observabilidad_costes.py"
        spec = importlib.util.spec_from_file_location("dash_v21", ruta)
        modulo = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(modulo)
        cls.modulo = modulo

    def test_render_get_base(self):
        ctx = self.modulo.construir_contexto("uso_normal_controlado")
        html = self.modulo.render_html(ctx)
        self.assertIn("Laboratorio V2.1", html)
        self.assertIn("Qué demuestra técnicamente", html)
        self.assertIn("Cómo lo usaría una empresa", html)

    def test_render_escenario_predefinido(self):
        ctx = self.modulo.construir_contexto("alta_latencia_critica")
        html = self.modulo.render_html(ctx)
        self.assertIn("alta_latencia_critica", html)
        self.assertIn("Total eventos", html)

    def test_render_entrada_manual_valida(self):
        eventos = [
            {
                "id_evento": "M-001",
                "caso_uso": "demo",
                "modelo": "local",
                "proveedor": "local",
                "tokens_entrada": 10,
                "tokens_salida": 5,
                "latencia_ms": 300,
                "coste_estimado_eur": 0.001,
                "estado": "ok",
                "riesgo": "bajo",
                "equipo": "equipo",
                "usuario": "u",
                "timestamp": "2026-05-13T00:00:00Z",
                "trazabilidad": "t",
            }
        ]
        ctx = self.modulo.construir_contexto("uso_normal_controlado", json.dumps(eventos, ensure_ascii=False))
        html = self.modulo.render_html(ctx)
        self.assertIn("M-001", html)
        self.assertEqual(ctx["error_parseo"], "")

    def test_render_entrada_manual_invalida(self):
        ctx = self.modulo.construir_contexto("uso_normal_controlado", "{json_invalido")
        html = self.modulo.render_html(ctx)
        self.assertIn("Entrada personalizada invalida", html)


if __name__ == "__main__":
    unittest.main()
