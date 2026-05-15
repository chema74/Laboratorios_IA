from __future__ import annotations

import importlib.util
from pathlib import Path


def cargar_modulo():
    ruta = Path(__file__).resolve().parents[1] / "scripts" / "validar_v2.py"
    spec = importlib.util.spec_from_file_location("validar_v2_gobernanza_ai_act", ruta)
    modulo = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(modulo)
    return modulo


def crear_estructura_minima(base: Path) -> None:
    docs = base / "docs"
    scripts = base / "scripts"
    tests = base / "tests"
    docs.mkdir()
    scripts.mkdir()
    tests.mkdir()

    licencia = (
        "\n\n---\n\n"
        "## 🪪 Licencia y Autoría\n"
        "Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.\n"
        "© 2025 – Txema Ríos. Todos los derechos compartidos.\n"
    )

    for nombre in [
        "PLAN_V2_LABORATORIO_GOBERNANZA_AI_ACT.md",
        "MAPA_EVIDENCIAS_V2.md",
        "LIMITES_ALCANCE_V2.md",
        "GUIA_REVISION_EVIDENCIAS_V2.md",
    ]:
        (docs / nombre).write_text(f"# {nombre}\n{licencia}", encoding="utf-8")

    (scripts / "demo.py").write_text("# demo\n", encoding="utf-8")
    (tests / "test_demo.py").write_text("def test_demo():\n    assert True\n", encoding="utf-8")


def test_construir_resultado_ok_con_estructura_minima(tmp_path):
    modulo = cargar_modulo()
    crear_estructura_minima(tmp_path)

    resultado = modulo.construir_resultado(tmp_path)

    assert resultado["resultado"] == "ok"
    assert resultado["web_publica"] == "no_modificada"
    assert resultado["main"] == "no_modificado"
    assert resultado["dependencias_externas_obligatorias"] == "ninguna"
    assert resultado["mojibake"] == []


def test_escribir_validacion_crea_markdown(tmp_path):
    modulo = cargar_modulo()
    crear_estructura_minima(tmp_path)

    resultado = modulo.construir_resultado(tmp_path)
    salida = tmp_path / "salidas" / "validacion_v2_gobernanza_ai_act.md"
    ruta = modulo.escribir_validacion(tmp_path, resultado, salida)

    assert ruta.exists()
    texto = ruta.read_text(encoding="utf-8")
    assert "VALIDACIÓN V2" in texto
    assert "VALIDACION_V2_GOBERNANZA_AI_ACT: OK" in texto
    assert "WEB_PUBLICA: NO_MODIFICADA" in texto
    assert "## 🪪 Licencia y Autoría" in texto