from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

RUTA_BASE = Path(__file__).resolve().parents[1]
RUTA_SRC = RUTA_BASE / "src"
if str(RUTA_SRC) not in sys.path:
    sys.path.insert(0, str(RUTA_SRC))

from fabrica_documentos_sinteticos.cargador_contexto import cargar_contexto
from fabrica_documentos_sinteticos.exportador import exportar_documentos
from fabrica_documentos_sinteticos.generador import construir_resumen_documentos, generar_documentos_sinteticos

TIPOS_MINIMOS = {
    "propuesta_comercial",
    "contrato_simulado",
    "correo_cliente",
    "acta_reunion",
    "informe_operativo",
    "ticket_soporte",
    "politica_interna",
}


def _tmp_local(nombre: str) -> Path:
    base = RUTA_BASE / "tests" / ".tmp"
    base.mkdir(parents=True, exist_ok=True)
    ruta = base / nombre
    if ruta.exists():
        shutil.rmtree(ruta)
    ruta.mkdir(parents=True, exist_ok=True)
    return ruta


def test_devuelve_lista_documentos():
    contexto = cargar_contexto("no_existe_empresa.json", "no_existe_eventos.json")
    docs = generar_documentos_sinteticos(contexto, seed=42, documentos_por_tipo=1)
    assert isinstance(docs, list)
    assert len(docs) == len(TIPOS_MINIMOS)


def test_reproducible_misma_seed():
    contexto = cargar_contexto("no_existe_empresa.json", "no_existe_eventos.json")
    a = generar_documentos_sinteticos(contexto, seed=99, documentos_por_tipo=1)
    b = generar_documentos_sinteticos(contexto, seed=99, documentos_por_tipo=1)
    assert a == b


def test_tipos_minimos_generados():
    contexto = cargar_contexto("no_existe_empresa.json", "no_existe_eventos.json")
    docs = generar_documentos_sinteticos(contexto, seed=10, documentos_por_tipo=1)
    tipos = {d["tipo_documento"] for d in docs}
    assert TIPOS_MINIMOS.issubset(tipos)


def test_metadatos_obligatorios_y_aviso():
    contexto = cargar_contexto("no_existe_empresa.json", "no_existe_eventos.json")
    doc = generar_documentos_sinteticos(contexto, seed=1, documentos_por_tipo=1)[0]
    obligatorios = {
        "id_documento", "tipo_documento", "titulo", "fecha_documento", "entidad_relacionada",
        "id_entidad_relacionada", "origen_simulado", "nivel_sensibilidad_ficticia",
        "requiere_revision_humana", "ruta_markdown", "estado_documento",
    }
    assert obligatorios.issubset(doc.keys())
    assert "documento sintético" in doc["contenido_markdown"].lower() or "documento sintético" in doc["contenido_markdown"].lower()


def test_exportacion_indice_resumen_y_markdown():
    contexto = cargar_contexto("no_existe_empresa.json", "no_existe_eventos.json")
    docs = generar_documentos_sinteticos(contexto, seed=2, documentos_por_tipo=1)
    resumen = construir_resumen_documentos(docs, {"entrada_empresa": "x", "entrada_eventos": "y"})
    salida = _tmp_local("exportacion")

    rutas = exportar_documentos(docs, resumen, salida)
    assert Path(rutas["indice_documentos"]).exists()
    assert Path(rutas["resumen_documentos"]).exists()

    md_files = list(salida.rglob("*.md"))
    assert len(md_files) >= len(TIPOS_MINIMOS)


def test_funciona_sin_archivos_previos():
    contexto = cargar_contexto("archivo_no_disponible_empresa.json", "archivo_no_disponible_eventos.json")
    docs = generar_documentos_sinteticos(contexto, seed=3, documentos_por_tipo=1)
    assert len(docs) > 0


def test_sin_api_claves_datos_reales_pdf_docx():
    contexto = cargar_contexto("no_existe_empresa.json", "no_existe_eventos.json")
    docs = generar_documentos_sinteticos(contexto, seed=4, documentos_por_tipo=1)
    texto = json.dumps(docs, ensure_ascii=False).lower()
    assert "api_key" not in texto
    assert "token" not in texto
    assert "password" not in texto
    assert ".pdf" not in texto
    assert ".docx" not in texto
    assert "ficticio" in texto or "sintetico" in texto
