# -*- coding: utf-8 -*-
"""Tests del informe ejecutivo V2 de privacidad de datos IA."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]


def test_generar_informe_ejecutivo_v2_devuelve_ok_y_genera_markdown():
    resultado = subprocess.run(
        [sys.executable, "scripts/generar_informe_ejecutivo_v2.py", "--json"],
        cwd=REPO,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )

    assert resultado.returncode == 0, resultado.stderr
    datos = json.loads(resultado.stdout)
    assert datos["resultado"] == "OK"
    assert datos["datos_reales"] == "NO"
    assert datos["sin_datos_personales_reales"] == "SI"

    informe = REPO / "salidas" / "informe_ejecutivo_v2.md"
    assert informe.exists()
    texto = informe.read_text(encoding="utf-8")
    assert "WEB_PUBLICA: NO_MODIFICADA" in texto
    assert "© 2025 – Txema Ríos. Todos los derechos compartidos." in texto
