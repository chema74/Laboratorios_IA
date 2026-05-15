"""Tests del validador V2 del laboratorio backend IA empresarial."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def test_validar_v2_devuelve_ok_y_genera_evidencia():
    result = subprocess.run(
        [sys.executable, "scripts/validar_v2.py", "--json"],
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
    assert data["web_publica"] == "NO_MODIFICADA"
    assert (REPO / "salidas" / "validacion_v2.md").exists()
