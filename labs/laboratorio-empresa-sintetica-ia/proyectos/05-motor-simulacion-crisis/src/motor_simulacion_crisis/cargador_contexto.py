"""Carga de contexto desde artefactos previos con fallback interno."""

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
        "clientes": [{"id_cliente": "CLI-0001"}, {"id_cliente": "CLI-0002"}],
        "procesos": [{"id_proceso": "PROC-001"}, {"id_proceso": "PROC-002"}],
    }


def _fallback_eventos() -> list[dict]:
    return [
        {"id_evento": "EVT-000001", "tipo_evento": "pago_pendiente", "severidad": "media"},
        {"id_evento": "EVT-000002", "tipo_evento": "reclamacion_cliente", "severidad": "alta"},
    ]


def _fallback_documentos() -> list[dict]:
    return [
        {"id_documento": "DOC-000001", "tipo_documento": "informe_operativo"},
        {"id_documento": "DOC-000002", "tipo_documento": "politica_interna"},
    ]


def _fallback_escenarios() -> list[dict]:
    return [
        {"id_escenario": "ESC-000001", "tipo_escenario": "escenario_operativo"},
        {"id_escenario": "ESC-000002", "tipo_escenario": "escenario_privacidad"},
    ]


def cargar_contexto(ruta_empresa: str, ruta_eventos: str, ruta_documentos: str, ruta_escenarios: str) -> dict:
    """
    1) Carga JSON de entradas previas si existen.
    2) Usa fallback interno mínimo cuando falten.
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

    escenarios = _leer_json(ruta_escenarios)
    if not isinstance(escenarios, list):
        escenarios = _fallback_escenarios()

    return {
        "empresa": empresa,
        "eventos": eventos,
        "documentos": documentos,
        "escenarios": escenarios,
    }
