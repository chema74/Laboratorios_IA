"""Carga de contexto desde proyectos previos con fallback interno."""

from __future__ import annotations

import json
from pathlib import Path


def _leer_json(ruta: str | Path) -> object | None:
    archivo = Path(ruta)
    if not archivo.exists() or not archivo.is_file():
        return None
    try:
        return json.loads(archivo.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _fallback_empresa() -> dict:
    return {
        "empresa": {"id_empresa": "EMP-FALLBACK-0001", "nombre": "Empresa Sintetica Fallback", "sector": "Servicios"},
        "clientes": [{"id_cliente": "CLI-0001", "estado": "activo"}, {"id_cliente": "CLI-0002", "estado": "en_riesgo"}],
        "procesos": [{"id_proceso": "PROC-001", "criticidad": "Alta"}],
    }


def _fallback_eventos() -> list[dict]:
    return [
        {"id_evento": "EVT-000001", "tipo_evento": "pago_pendiente", "severidad": "media", "id_entidad_afectada": "CLI-0001"},
        {"id_evento": "EVT-000002", "tipo_evento": "reclamacion_cliente", "severidad": "alta", "id_entidad_afectada": "CLI-0002"},
    ]


def _fallback_documentos() -> list[dict]:
    return [
        {"id_documento": "DOC-000001", "tipo_documento": "informe_operativo", "id_entidad_relacionada": "CLI-0001"},
        {"id_documento": "DOC-000002", "tipo_documento": "politica_interna", "id_entidad_relacionada": "CLI-0002"},
    ]


def cargar_contexto(ruta_empresa: str | Path, ruta_eventos: str | Path, ruta_documentos: str | Path) -> dict:
    """
    1) Intenta cargar empresa, eventos e índice documental.
    2) Si falta alguna entrada, aplica fallback interno mínimo.
    """
    empresa = _leer_json(ruta_empresa)
    if not isinstance(empresa, dict) or "empresa" not in empresa:
        empresa = _fallback_empresa()

    eventos = _leer_json(ruta_eventos)
    if not isinstance(eventos, list):
        eventos = _fallback_eventos()

    documentos = _leer_json(ruta_documentos)
    if not isinstance(documentos, list):
        documentos = _fallback_documentos()

    return {"empresa": empresa, "eventos": eventos, "documentos": documentos}
