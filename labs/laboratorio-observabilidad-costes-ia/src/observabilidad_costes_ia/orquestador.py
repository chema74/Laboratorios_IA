from __future__ import annotations

import os
from typing import Any

from .analisis_local import generar_analisis_fallback
from .integracion_groq import MODELO_POR_DEFECTO, GroqError, analizar_con_groq


def _diagnostico_no_solicitado() -> dict[str, Any]:
    return {
        "solicitado": False,
        "estado": "no_solicitado",
        "categoria": "modo_fallback_forzado",
        "http_status": None,
        "modelo_usado": None,
        "mensaje_seguro": "El análisis se ejecutó en modo fallback local por configuración.",
    }



def _diagnostico_falta_clave(modelo: str) -> dict[str, Any]:
    return {
        "solicitado": True,
        "estado": "fallo",
        "categoria": "falta_clave",
        "http_status": None,
        "modelo_usado": modelo,
        "mensaje_seguro": "No se encontró GROQ_API_KEY en el entorno.",
    }



def generar_analisis_ejecutivo(metrica: dict[str, Any]) -> dict[str, Any]:
    modo_cfg = os.environ.get("OBSERVABILIDAD_MODO", "").strip().lower()
    modo_solicitado_groq = modo_cfg == "groq"
    modelo = os.environ.get("GROQ_MODEL", MODELO_POR_DEFECTO).strip() or MODELO_POR_DEFECTO

    if modo_cfg == "fallback_local":
        analisis = generar_analisis_fallback(metrica)
        analisis["diagnostico_groq"] = _diagnostico_no_solicitado()
        return analisis

    if modo_solicitado_groq and not os.environ.get("GROQ_API_KEY", "").strip():
        analisis = generar_analisis_fallback(metrica)
        analisis["diagnostico_groq"] = _diagnostico_falta_clave(modelo)
        return analisis

    if not modo_solicitado_groq:
        analisis = generar_analisis_fallback(metrica)
        analisis["diagnostico_groq"] = {
            "solicitado": False,
            "estado": "no_solicitado",
            "categoria": "modo_no_groq",
            "http_status": None,
            "modelo_usado": None,
            "mensaje_seguro": "No se solicitó modo groq; se ejecutó fallback local.",
        }
        return analisis

    try:
        analisis_groq = analizar_con_groq(metrica)
        analisis_groq["diagnostico_groq"] = {
            "solicitado": True,
            "estado": "ok",
            "categoria": "groq_ok",
            "http_status": int(analisis_groq.get("http_status_groq", 200)),
            "modelo_usado": analisis_groq.get("modelo_groq", modelo),
            "mensaje_seguro": "Análisis generado correctamente mediante Groq.",
        }
        return analisis_groq
    except GroqError as exc:
        analisis = generar_analisis_fallback(metrica)
        analisis["diagnostico_groq"] = {
            "solicitado": True,
            "estado": "fallo",
            "categoria": exc.categoria,
            "http_status": exc.http_status,
            "modelo_usado": exc.modelo or modelo,
            "mensaje_seguro": exc.mensaje_seguro,
        }
        return analisis
