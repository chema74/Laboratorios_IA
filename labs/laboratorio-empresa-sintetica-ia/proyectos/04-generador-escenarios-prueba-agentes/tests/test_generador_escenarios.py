from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

RUTA_BASE = Path(__file__).resolve().parents[1]
RUTA_SRC = RUTA_BASE / "src"
if str(RUTA_SRC) not in sys.path:
    sys.path.insert(0, str(RUTA_SRC))

from generador_escenarios_prueba_agentes.cargador_contexto import cargar_contexto
from generador_escenarios_prueba_agentes.catalogo_escenarios import (
    ACCIONES_CONTROLADAS,
    DIFICULTADES_CONTROLADAS,
    TIPOS_ESCENARIO,
)
from generador_escenarios_prueba_agentes.exportador import exportar_escenarios
from generador_escenarios_prueba_agentes.generador import construir_resumen_escenarios, generar_escenarios

OBLIGATORIOS = {
    "id_escenario", "tipo_escenario", "titulo", "descripcion", "contexto_empresarial", "entrada_usuario_simulada",
    "objetivo_del_agente", "datos_disponibles", "restricciones", "riesgos_detectables", "comportamiento_esperado",
    "accion_recomendada", "requiere_revision_humana", "nivel_dificultad", "criterio_evaluacion", "etiquetas", "origen_simulado",
}


def _tmp_local(nombre: str) -> Path:
    base = RUTA_BASE / "tests" / ".tmp"
    base.mkdir(parents=True, exist_ok=True)
    ruta = base / nombre
    if ruta.exists():
        shutil.rmtree(ruta)
    ruta.mkdir(parents=True, exist_ok=True)
    return ruta


def test_lista_escenarios():
    ctx = cargar_contexto("x.json", "y.json", "z.json")
    esc = generar_escenarios(ctx, seed=42, escenarios_por_tipo=1)
    assert isinstance(esc, list)
    assert len(esc) == len(TIPOS_ESCENARIO)


def test_reproducibilidad_seed():
    ctx = cargar_contexto("x.json", "y.json", "z.json")
    a = generar_escenarios(ctx, seed=99, escenarios_por_tipo=1)
    b = generar_escenarios(ctx, seed=99, escenarios_por_tipo=1)
    assert a == b


def test_tipos_minimos_presentes():
    ctx = cargar_contexto("x.json", "y.json", "z.json")
    esc = generar_escenarios(ctx, seed=7, escenarios_por_tipo=1)
    tipos = {e["tipo_escenario"] for e in esc}
    assert set(TIPOS_ESCENARIO).issubset(tipos)


def test_campos_obligatorios():
    ctx = cargar_contexto("x.json", "y.json", "z.json")
    e = generar_escenarios(ctx, seed=1, escenarios_por_tipo=1)[0]
    assert OBLIGATORIOS.issubset(e.keys())


def test_acciones_y_dificultades_controladas():
    ctx = cargar_contexto("x.json", "y.json", "z.json")
    esc = generar_escenarios(ctx, seed=11, escenarios_por_tipo=2)
    assert all(e["accion_recomendada"] in ACCIONES_CONTROLADAS for e in esc)
    assert all(e["nivel_dificultad"] in DIFICULTADES_CONTROLADAS for e in esc)


def test_hay_revision_humana_y_tipos_criticos():
    ctx = cargar_contexto("x.json", "y.json", "z.json")
    esc = generar_escenarios(ctx, seed=12, escenarios_por_tipo=1)
    assert any(e["requiere_revision_humana"] for e in esc)
    tipos = {e["tipo_escenario"] for e in esc}
    assert "escenario_peligroso" in tipos or "escenario_privacidad" in tipos


def test_exportaciones_json_csv_resumen_markdown():
    ctx = cargar_contexto("x.json", "y.json", "z.json")
    esc = generar_escenarios(ctx, seed=3, escenarios_por_tipo=1)
    resumen = construir_resumen_escenarios(esc, {"entrada_empresa": "x", "entrada_eventos": "y", "entrada_documentos": "z"})
    salida = _tmp_local("export")
    rutas = exportar_escenarios(esc, resumen, salida)

    assert Path(rutas["escenarios_json"]).exists()
    assert Path(rutas["escenarios_csv"]).exists()
    assert Path(rutas["resumen_json"]).exists()
    md = list(Path(rutas["markdown_dir"]).glob("*.md"))
    assert len(md) == len(esc)


def test_fallback_y_sin_api_claves_datos_reales_y_sin_ejecucion_agentes():
    ctx = cargar_contexto("no_empresa.json", "no_eventos.json", "no_docs.json")
    esc = generar_escenarios(ctx, seed=5, escenarios_por_tipo=1)
    texto = json.dumps(esc, ensure_ascii=False).lower()
    assert "api_key" not in texto
    assert "token" not in texto
    assert "password" not in texto
    assert "ejecuta agentes reales" not in texto
