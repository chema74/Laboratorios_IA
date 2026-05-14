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
        "empresa": {
            "id_empresa": "EMP-FALLBACK-0001",
            "nombre": "Empresa Sintetica Fallback",
            "sector": "Servicios",
            "pais": "España",
            "ciudad": "Madrid",
        },
        "resumen_operativo": {
            "ingresos_estimados_mensuales": 120000.0,
            "tickets_abiertos": 8,
            "incidencias_activas": 4,
            "pagos_pendientes": 6,
            "alertas_operativas": 3,
        },
        "clientes": [{"id_cliente": "CLI-0001"}, {"id_cliente": "CLI-0002"}],
    }


def _fallback_eventos() -> list[dict]:
    return [
        {"id_evento": "EVT-000001", "tipo_evento": "pago_pendiente", "severidad": "media"},
        {"id_evento": "EVT-000002", "tipo_evento": "reclamacion_cliente", "severidad": "alta"},
        {"id_evento": "EVT-000003", "tipo_evento": "retraso_operativo", "severidad": "media"},
    ]


def _fallback_documentos() -> list[dict]:
    return [
        {"id_documento": "DOC-000001", "tipo_documento": "informe_operativo"},
        {"id_documento": "DOC-000002", "tipo_documento": "ticket_soporte"},
    ]


def _fallback_escenarios() -> list[dict]:
    return [
        {"id_escenario": "ESC-000001", "tipo_escenario": "escenario_operativo"},
        {"id_escenario": "ESC-000002", "tipo_escenario": "escenario_privacidad"},
    ]


def _fallback_crisis() -> list[dict]:
    return [
        {"id_crisis": "CRS-00001", "tipo_crisis": "caida_ventas", "severidad": "alta", "estado_crisis": "en_revision"},
        {"id_crisis": "CRS-00002", "tipo_crisis": "incidente_privacidad", "severidad": "critica", "estado_crisis": "escalada"},
    ]


def _fallback_revisiones() -> list[dict]:
    return [
        {"id_revision": "REV-000001", "decision": "escalar", "requiere_segunda_revision": True},
        {"id_revision": "REV-000002", "decision": "aceptar", "requiere_segunda_revision": False},
    ]


def _fallback_registro_decisiones() -> list[dict]:
    return [
        {"id_registro": "REG-000001", "estado_registro": "pendiente"},
        {"id_registro": "REG-000002", "estado_registro": "escalado"},
    ]


def cargar_contexto(
    entrada_empresa: str,
    entrada_eventos: str,
    entrada_documentos: str,
    entrada_escenarios: str,
    entrada_crisis: str,
    entrada_revisiones: str,
    entrada_registro_decisiones: str,
) -> dict:
    """
    1) Carga cada entrada si existe.
    2) Si falta, utiliza fallback interno mínimo.
    """
    empresa = _leer_json(entrada_empresa)
    if not isinstance(empresa, dict) or "empresa" not in empresa:
        empresa = _fallback_empresa()

    eventos = _leer_json(entrada_eventos)
    if not isinstance(eventos, list):
        eventos = _fallback_eventos()

    documentos = _leer_json(entrada_documentos)
    if not isinstance(documentos, list):
        documentos = _fallback_documentos()

    escenarios = _leer_json(entrada_escenarios)
    if not isinstance(escenarios, list):
        escenarios = _fallback_escenarios()

    crisis = _leer_json(entrada_crisis)
    if not isinstance(crisis, list):
        crisis = _fallback_crisis()

    revisiones = _leer_json(entrada_revisiones)
    if not isinstance(revisiones, list):
        revisiones = _fallback_revisiones()

    registro = _leer_json(entrada_registro_decisiones)
    if not isinstance(registro, list):
        registro = _fallback_registro_decisiones()

    return {
        "empresa": empresa,
        "eventos": eventos,
        "documentos": documentos,
        "escenarios": escenarios,
        "crisis": crisis,
        "revisiones": revisiones,
        "registro_decisiones": registro,
    }
