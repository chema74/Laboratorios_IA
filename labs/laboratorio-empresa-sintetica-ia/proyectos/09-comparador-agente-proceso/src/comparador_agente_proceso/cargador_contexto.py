"""Carga de contexto desde proyectos previos con fallback interno."""

from __future__ import annotations

import json
from pathlib import Path


def _leer_json(ruta: str | Path) -> object | None:
    p = Path(ruta)
    if not p.exists() or not p.is_file():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _fallback() -> dict:
    return {
        "empresa": {"empresa": {"id_empresa": "EMP-FALLBACK", "nombre": "Empresa Sintetica Fallback"}},
        "eventos": [{"id_evento": "EVT-1", "tipo_evento": "pago_pendiente"}],
        "documentos": [{"id_documento": "DOC-1", "tipo_documento": "informe_operativo"}],
        "escenarios": [{"id_escenario": "ESC-1", "tipo_escenario": "escenario_operativo"}],
        "crisis": [{"id_crisis": "CRS-1", "tipo_crisis": "caida_ventas", "severidad": "alta"}],
        "revisiones": [{"id_revision": "REV-1", "decision": "escalar"}],
        "registro_decisiones": [{"id_registro": "REG-1", "estado_registro": "pendiente"}],
        "estado_operativo": {"metricas_operativas": {"indice_riesgo_simulado": 60}},
        "alertas": [{"id_alerta": "ALT-1", "severidad": "alta"}],
        "decisiones": [{"id_decision": "DEC-1", "estado_decision": "escalada"}],
        "inventario_privacidad": [{"id_dato": "DAT-1", "nivel_sensibilidad_ficticia": "confidencial"}],
        "riesgos_privacidad": [{"id_riesgo": "RGS-1", "severidad": "alta"}],
    }


def cargar_contexto(paths: dict[str, str]) -> dict:
    f = _fallback()
    loaded = {
        "empresa": _leer_json(paths["entrada_empresa"]),
        "eventos": _leer_json(paths["entrada_eventos"]),
        "documentos": _leer_json(paths["entrada_documentos"]),
        "escenarios": _leer_json(paths["entrada_escenarios"]),
        "crisis": _leer_json(paths["entrada_crisis"]),
        "revisiones": _leer_json(paths["entrada_revisiones"]),
        "registro_decisiones": _leer_json(paths["entrada_registro_decisiones"]),
        "estado_operativo": _leer_json(paths["entrada_estado_operativo"]),
        "alertas": _leer_json(paths["entrada_alertas"]),
        "decisiones": _leer_json(paths["entrada_decisiones"]),
        "inventario_privacidad": _leer_json(paths["entrada_inventario_privacidad"]),
        "riesgos_privacidad": _leer_json(paths["entrada_riesgos_privacidad"]),
    }

    return {
        "empresa": loaded["empresa"] if isinstance(loaded["empresa"], dict) else f["empresa"],
        "eventos": loaded["eventos"] if isinstance(loaded["eventos"], list) else f["eventos"],
        "documentos": loaded["documentos"] if isinstance(loaded["documentos"], list) else f["documentos"],
        "escenarios": loaded["escenarios"] if isinstance(loaded["escenarios"], list) else f["escenarios"],
        "crisis": loaded["crisis"] if isinstance(loaded["crisis"], list) else f["crisis"],
        "revisiones": loaded["revisiones"] if isinstance(loaded["revisiones"], list) else f["revisiones"],
        "registro_decisiones": loaded["registro_decisiones"] if isinstance(loaded["registro_decisiones"], list) else f["registro_decisiones"],
        "estado_operativo": loaded["estado_operativo"] if isinstance(loaded["estado_operativo"], dict) else f["estado_operativo"],
        "alertas": loaded["alertas"] if isinstance(loaded["alertas"], list) else f["alertas"],
        "decisiones": loaded["decisiones"] if isinstance(loaded["decisiones"], list) else f["decisiones"],
        "inventario_privacidad": loaded["inventario_privacidad"] if isinstance(loaded["inventario_privacidad"], list) else f["inventario_privacidad"],
        "riesgos_privacidad": loaded["riesgos_privacidad"] if isinstance(loaded["riesgos_privacidad"], list) else f["riesgos_privacidad"],
    }
