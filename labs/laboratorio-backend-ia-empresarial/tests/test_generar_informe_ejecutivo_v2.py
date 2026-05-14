# -*- coding: utf-8 -*-
"""Tests del informe ejecutivo V2 del laboratorio backend IA empresarial."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def test_generar_informe_ejecutivo_v2_devuelve_ok_y_genera_markdown():
    result = subprocess.run(
        [sys.executable, "scripts/generar_informe_ejecutivo_v2.py", "--json"],
        cwd=REPO,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )

    assert result.returncode == 0, result.stderr
    data = json.loads(result.stdout)
    assert data["resultado"] == "OK"
    assert data["local_first"] == "SI"
    assert data["free_first"] == "SI"

    report = REPO / "salidas" / "informe_ejecutivo_v2.md"
    assert report.exists()
    text = report.read_text(encoding="utf-8")
    assert "WEB_PUBLICA: NO_MODIFICADA" in text
    assert "© 2025 – Txema Ríos. Todos los derechos compartidos." in text
