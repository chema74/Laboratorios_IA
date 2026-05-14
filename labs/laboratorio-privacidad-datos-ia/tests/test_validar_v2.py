# -*- coding: utf-8 -*-
"""Tests del validador V2 de privacidad de datos IA."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]


def test_validar_v2_devuelve_ok_y_genera_evidencia():
    resultado = subprocess.run(
        [sys.executable, "scripts/validar_v2.py", "--json"],
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
    assert datos["web_publica"] == "NO_MODIFICADA"
    assert (REPO / "salidas" / "validacion_v2.md").exists()
