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


def _fallback_contexto() -> dict:
    return {
        "empresa": {
            "empresa": {"id_empresa": "EMP-FALLBACK-0001", "nombre": "Empresa Sintetica Fallback", "sector": "Servicios", "pais": "España", "ciudad": "Madrid"},
            "clientes": [{"id_cliente": "CLI-0001", "nombre": "Cliente Ficticio 1", "estado": "activo"}],
            "empleados": [{"id_empleado": "EMPLO-0001", "nombre": "Empleado Ficticio 1", "departamento": "Operaciones"}],
            "productos": [{"id_producto": "PROD-0001", "nombre": "Producto Sintetico 1"}],
        },
        "eventos": [{"id_evento": "EVT-000001", "tipo_evento": "pago_pendiente", "descripcion": "Evento ficticio"}],
        "documentos": [{"id_documento": "DOC-000001", "tipo_documento": "informe_operativo"}],
        "escenarios": [{"id_escenario": "ESC-000001", "tipo_escenario": "escenario_privacidad"}],
        "crisis": [{"id_crisis": "CRS-00001", "tipo_crisis": "incidente_privacidad", "severidad": "alta"}],
        "revisiones": [{"id_revision": "REV-000001", "decision": "escalar", "requiere_segunda_revision": True}],
        "registro_decisiones": [{"id_registro": "REG-000001", "estado_registro": "pendiente"}],
        "estado_operativo": {"identidad_empresa": {"id_empresa": "EMP-FALLBACK-0001"}, "metricas_operativas": {"indice_riesgo_simulado": 55.0}},
        "alertas_operativas": [{"id_alerta": "ALT-00001", "severidad": "alta", "area_afectada": "privacidad"}],
        "decisiones_simuladas": [{"id_decision": "DEC-00001", "estado_decision": "escalada"}],
    }


def cargar_contexto(
    entrada_empresa: str,
    entrada_eventos: str,
    entrada_documentos: str,
    entrada_escenarios: str,
    entrada_crisis: str,
    entrada_revisiones: str,
    entrada_registro_decisiones: str,
    entrada_estado_operativo: str,
    entrada_alertas: str,
    entrada_decisiones: str,
) -> dict:
    """
    1) Carga JSON de entradas previas si existen.
    2) Aplica fallback interno mínimo cuando faltan entradas.
    """
    fallback = _fallback_contexto()

    empresa = _leer_json(entrada_empresa)
    eventos = _leer_json(entrada_eventos)
    documentos = _leer_json(entrada_documentos)
    escenarios = _leer_json(entrada_escenarios)
    crisis = _leer_json(entrada_crisis)
    revisiones = _leer_json(entrada_revisiones)
    registro = _leer_json(entrada_registro_decisiones)
    estado = _leer_json(entrada_estado_operativo)
    alertas = _leer_json(entrada_alertas)
    decisiones = _leer_json(entrada_decisiones)

    return {
        "empresa": empresa if isinstance(empresa, dict) else fallback["empresa"],
        "eventos": eventos if isinstance(eventos, list) else fallback["eventos"],
        "documentos": documentos if isinstance(documentos, list) else fallback["documentos"],
        "escenarios": escenarios if isinstance(escenarios, list) else fallback["escenarios"],
        "crisis": crisis if isinstance(crisis, list) else fallback["crisis"],
        "revisiones": revisiones if isinstance(revisiones, list) else fallback["revisiones"],
        "registro_decisiones": registro if isinstance(registro, list) else fallback["registro_decisiones"],
        "estado_operativo": estado if isinstance(estado, dict) else fallback["estado_operativo"],
        "alertas_operativas": alertas if isinstance(alertas, list) else fallback["alertas_operativas"],
        "decisiones_simuladas": decisiones if isinstance(decisiones, list) else fallback["decisiones_simuladas"],
    }
