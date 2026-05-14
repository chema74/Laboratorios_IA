"""Carga de eventos, documentos, escenarios y crisis con fallback."""

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


def _fallback_eventos() -> list[dict]:
    return [
        {"id_evento": "EVT-000001", "tipo_evento": "pago_pendiente", "descripcion": "Evento sintético de pago pendiente."},
        {"id_evento": "EVT-000002", "tipo_evento": "reclamacion_cliente", "descripcion": "Evento sintético de reclamación."},
    ]


def _fallback_documentos() -> list[dict]:
    return [
        {"id_documento": "DOC-000001", "tipo_documento": "informe_operativo", "titulo": "Informe Operativo Ficticio"},
        {"id_documento": "DOC-000002", "tipo_documento": "politica_interna", "titulo": "Política Interna Ficticia"},
    ]


def _fallback_escenarios() -> list[dict]:
    return [
        {"id_escenario": "ESC-000001", "tipo_escenario": "escenario_operativo", "titulo": "Escenario Operativo Ficticio"},
        {"id_escenario": "ESC-000002", "tipo_escenario": "escenario_privacidad", "titulo": "Escenario Privacidad Ficticio"},
    ]


def _fallback_crisis() -> list[dict]:
    return [
        {"id_crisis": "CRS-00001", "tipo_crisis": "incidente_privacidad", "titulo": "Crisis de Privacidad Ficticia"},
        {"id_crisis": "CRS-00002", "tipo_crisis": "datos_corruptos", "titulo": "Crisis de Datos Corruptos Ficticia"},
    ]


def cargar_contexto(ruta_eventos: str, ruta_documentos: str, ruta_escenarios: str, ruta_crisis: str) -> dict:
    """
    1) Carga entradas previas si existen.
    2) Si faltan, usa fallback interno mínimo.
    """
    eventos = _leer_json(ruta_eventos)
    if not isinstance(eventos, list):
        eventos = _fallback_eventos()

    documentos = _leer_json(ruta_documentos)
    if not isinstance(documentos, list):
        documentos = _fallback_documentos()

    escenarios = _leer_json(ruta_escenarios)
    if not isinstance(escenarios, list):
        escenarios = _fallback_escenarios()

    crisis = _leer_json(ruta_crisis)
    if not isinstance(crisis, list):
        crisis = _fallback_crisis()

    return {
        "eventos": eventos,
        "documentos": documentos,
        "escenarios": escenarios,
        "crisis": crisis,
    }
