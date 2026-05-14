"""Carga de contexto desde artefactos previos con fallback interno."""

from __future__ import annotations

import json
from pathlib import Path


def _leer_json(ruta: str | Path) -> object | None:
    path = Path(ruta)
    if not path.exists() or not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _fallback() -> dict:
    return {
        "empresa": {"empresa": {"id_empresa": "EMP-FALLBACK", "nombre": "Empresa Sintetica Fallback", "sector": "servicios"}},
        "eventos": [{"id_evento": "EVT-0001", "tipo_evento": "pago_pendiente", "severidad": "media"}],
        "resumen_eventos": {"total_eventos": 1},
        "documentos": [{"id_documento": "DOC-0001", "tipo_documento": "informe_operativo"}],
        "resumen_documentos": {"total_documentos": 1},
        "escenarios": [{"id_escenario": "ESC-0001", "tipo_escenario": "escenario_operativo"}],
        "resumen_escenarios": {"total_escenarios": 1},
        "crisis": [{"id_crisis": "CRS-0001", "tipo_crisis": "caida_ventas", "severidad": "alta"}],
        "resumen_crisis": {"total_crisis": 1},
        "revisiones": [{"id_revision": "REV-0001", "decision": "escalar"}],
        "registro_decisiones": [{"id_registro": "REG-0001", "estado_registro": "pendiente"}],
        "resumen_revision": {"total_revisiones": 1},
        "estado_operativo": {"empresa": {"nombre": "Empresa Sintetica Fallback"}},
        "alertas": [{"id_alerta": "ALT-0001", "severidad": "alta"}],
        "decisiones": [{"id_decision": "DEC-0001", "estado_decision": "pendiente_revision"}],
        "resumen_gemelo": {"total_alertas": 1},
        "inventario_privacidad": [{"id_dato": "DAT-0001", "nivel_sensibilidad_ficticia": "confidencial"}],
        "riesgos_privacidad": [{"id_riesgo": "RGS-0001", "severidad": "alta"}],
        "resumen_privacidad": {"total_datos_inventariados": 1},
        "procesos_comparados": [{"id_proceso_comparado": "PRC-0001", "nombre_proceso": "revision_reclamacion_cliente"}],
        "comparaciones": [{"id_comparacion": "CMP-0001", "flujo_recomendado_simulado": "hibrido_con_revision_humana"}],
        "resumen_comparador": {"total_procesos_comparados": 1},
    }


def cargar_contexto(paths: dict[str, str]) -> dict:
    fallback = _fallback()
    cargado = {clave: _leer_json(ruta) for clave, ruta in paths.items()}

    return {
        "empresa": cargado["entrada_empresa"] if isinstance(cargado["entrada_empresa"], dict) else fallback["empresa"],
        "eventos": cargado["entrada_eventos"] if isinstance(cargado["entrada_eventos"], list) else fallback["eventos"],
        "resumen_eventos": cargado["entrada_resumen_eventos"] if isinstance(cargado["entrada_resumen_eventos"], dict) else fallback["resumen_eventos"],
        "documentos": cargado["entrada_documentos"] if isinstance(cargado["entrada_documentos"], list) else fallback["documentos"],
        "resumen_documentos": cargado["entrada_resumen_documentos"] if isinstance(cargado["entrada_resumen_documentos"], dict) else fallback["resumen_documentos"],
        "escenarios": cargado["entrada_escenarios"] if isinstance(cargado["entrada_escenarios"], list) else fallback["escenarios"],
        "resumen_escenarios": cargado["entrada_resumen_escenarios"] if isinstance(cargado["entrada_resumen_escenarios"], dict) else fallback["resumen_escenarios"],
        "crisis": cargado["entrada_crisis"] if isinstance(cargado["entrada_crisis"], list) else fallback["crisis"],
        "resumen_crisis": cargado["entrada_resumen_crisis"] if isinstance(cargado["entrada_resumen_crisis"], dict) else fallback["resumen_crisis"],
        "revisiones": cargado["entrada_revisiones"] if isinstance(cargado["entrada_revisiones"], list) else fallback["revisiones"],
        "registro_decisiones": cargado["entrada_registro_decisiones"] if isinstance(cargado["entrada_registro_decisiones"], list) else fallback["registro_decisiones"],
        "resumen_revision": cargado["entrada_resumen_revision"] if isinstance(cargado["entrada_resumen_revision"], dict) else fallback["resumen_revision"],
        "estado_operativo": cargado["entrada_estado_operativo"] if isinstance(cargado["entrada_estado_operativo"], dict) else fallback["estado_operativo"],
        "alertas": cargado["entrada_alertas"] if isinstance(cargado["entrada_alertas"], list) else fallback["alertas"],
        "decisiones": cargado["entrada_decisiones"] if isinstance(cargado["entrada_decisiones"], list) else fallback["decisiones"],
        "resumen_gemelo": cargado["entrada_resumen_gemelo"] if isinstance(cargado["entrada_resumen_gemelo"], dict) else fallback["resumen_gemelo"],
        "inventario_privacidad": cargado["entrada_inventario_privacidad"] if isinstance(cargado["entrada_inventario_privacidad"], list) else fallback["inventario_privacidad"],
        "riesgos_privacidad": cargado["entrada_riesgos_privacidad"] if isinstance(cargado["entrada_riesgos_privacidad"], list) else fallback["riesgos_privacidad"],
        "resumen_privacidad": cargado["entrada_resumen_privacidad"] if isinstance(cargado["entrada_resumen_privacidad"], dict) else fallback["resumen_privacidad"],
        "procesos_comparados": cargado["entrada_procesos_comparados"] if isinstance(cargado["entrada_procesos_comparados"], list) else fallback["procesos_comparados"],
        "comparaciones": cargado["entrada_comparaciones"] if isinstance(cargado["entrada_comparaciones"], list) else fallback["comparaciones"],
        "resumen_comparador": cargado["entrada_resumen_comparador"] if isinstance(cargado["entrada_resumen_comparador"], dict) else fallback["resumen_comparador"],
    }

