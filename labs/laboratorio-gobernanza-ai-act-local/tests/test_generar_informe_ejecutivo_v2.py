# -*- coding: utf-8 -*-
from __future__ import annotations

import importlib.util
from pathlib import Path


def cargar_modulo():
    ruta = Path(__file__).resolve().parents[1] / "scripts" / "generar_informe_ejecutivo_v2.py"
    spec = importlib.util.spec_from_file_location("generar_informe_ejecutivo_v2_gobernanza_ai_act", ruta)
    modulo = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(modulo)
    return modulo


def crear_estructura_minima(base: Path) -> None:
    docs = base / "docs"
    scripts = base / "scripts"
    tests = base / "tests"
    salidas = base / "salidas"
    docs.mkdir()
    scripts.mkdir()
    tests.mkdir()
    salidas.mkdir()

    for nombre in [
        "PLAN_V2_LABORATORIO_GOBERNANZA_AI_ACT.md",
        "MAPA_EVIDENCIAS_V2.md",
        "LIMITES_ALCANCE_V2.md",
        "GUIA_REVISION_EVIDENCIAS_V2.md",
    ]:
        (docs / nombre).write_text(f"# {nombre}\n\nContenido.\n", encoding="utf-8")

    (scripts / "validar_v2.py").write_text("# validar\n", encoding="utf-8")
    (tests / "test_validar_v2.py").write_text("def test_ok():\n    assert True\n", encoding="utf-8")
    (salidas / "validacion_v2_gobernanza_ai_act.md").write_text(
        "# Validación\n\n`VALIDACION_V2_GOBERNANZA_AI_ACT: OK`\n\n- `MOJIBAKE: OK`\n",
        encoding="utf-8",
    )


def test_construir_informe_incluye_estado_y_licencia(tmp_path):
    modulo = cargar_modulo()
    crear_estructura_minima(tmp_path)

    informe = modulo.construir_informe(tmp_path)

    assert "# 📌 INFORME EJECUTIVO V2" in informe
    assert "LABORATORIO GOBERNANZA AI ACT LOCAL" in informe
    assert "Resultado de validación V2 detectado: `OK`" in informe
    assert "WEB_PUBLICA: NO_MODIFICADA" in informe
    assert "MAIN: NO_MODIFICADO" in informe
    assert "ASESORIA_LEGAL: NO" in informe
    assert "## 🪪 Licencia y Autoría" in informe


def test_escribir_informe_crea_archivo_markdown(tmp_path):
    modulo = cargar_modulo()
    crear_estructura_minima(tmp_path)

    salida = tmp_path / "salidas" / "informe_ejecutivo_v2_gobernanza_ai_act.md"
    ruta = modulo.escribir_informe(tmp_path, salida)

    assert ruta.exists()
    texto = ruta.read_text(encoding="utf-8")
    assert "INFORME_EJECUTIVO_V2_GOBERNANZA_AI_ACT_GENERADO: OK" in texto
    assert "DEPENDENCIAS_EXTERNAS_OBLIGATORIAS: NINGUNA" in texto