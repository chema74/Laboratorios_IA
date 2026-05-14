"""Carga de contexto desde empresa y eventos con fallback interno."""

from __future__ import annotations

import json
from pathlib import Path


def _empresa_fallback() -> dict:
    return {
        "empresa": {"id_empresa": "EMP-FALLBACK-0001", "nombre": "Empresa Sintetica Fallback", "sector": "Servicios"},
        "clientes": [
            {"id_cliente": "CLI-0001", "nombre": "Cliente Ficticio 1", "estado": "activo"},
            {"id_cliente": "CLI-0002", "nombre": "Cliente Ficticio 2", "estado": "en_riesgo"},
        ],
        "empleados": [{"id_empleado": "EMPLO-0001", "nombre": "Empleado Ficticio 1"}],
        "productos": [{"id_producto": "PROD-0001", "nombre": "Producto Sintetico 1", "precio_base": 1000.0}],
        "procesos": [{"id_proceso": "PROC-001", "nombre": "Gestion de pedidos", "criticidad": "Alta"}],
    }


def _eventos_fallback() -> list[dict]:
    return [
        {
            "id_evento": "EVT-000001",
            "tipo_evento": "pedido_creado",
            "fecha_evento": "2026-01-01",
            "severidad": "media",
            "id_entidad_afectada": "CLI-0001",
            "descripcion": "Evento simulado de pedido.",
            "requiere_revision_humana": False,
        },
        {
            "id_evento": "EVT-000002",
            "tipo_evento": "reclamacion_cliente",
            "fecha_evento": "2026-01-01",
            "severidad": "alta",
            "id_entidad_afectada": "CLI-0002",
            "descripcion": "Evento simulado de reclamación.",
            "requiere_revision_humana": True,
        },
    ]


def _leer_json_si_existe(ruta: str | Path) -> object | None:
    archivo = Path(ruta)
    if not archivo.exists() or not archivo.is_file():
        return None
    try:
        return json.loads(archivo.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def cargar_contexto(ruta_empresa: str | Path, ruta_eventos: str | Path) -> dict:
    """
    1) Carga empresa y eventos desde JSON si existen.
    2) Si faltan o fallan, aplica fallback interno mínimo.
    """
    empresa = _leer_json_si_existe(ruta_empresa)
    if not isinstance(empresa, dict) or "empresa" not in empresa:
        empresa = _empresa_fallback()

    eventos = _leer_json_si_existe(ruta_eventos)
    if not isinstance(eventos, list):
        eventos = _eventos_fallback()

    return {"empresa": empresa, "eventos": eventos}
