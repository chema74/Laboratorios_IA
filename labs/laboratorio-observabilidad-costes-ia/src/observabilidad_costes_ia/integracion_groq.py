from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any
from urllib import error, request

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODELO_POR_DEFECTO = "llama-3.1-8b-instant"
USER_AGENT = "portfolio-observabilidad-costes-ia/2.1 Python-urllib"


@dataclass
class GroqError(Exception):
    categoria: str
    mensaje_seguro: str
    http_status: int | None = None
    modelo: str | None = None

    def __str__(self) -> str:
        return self.mensaje_seguro


def _build_prompt(metrica: dict[str, Any]) -> str:
    return (
        "Genera un analisis ejecutivo de observabilidad y costes de IA en espanol con formato JSON "
        "y claves exactas: resumen_ejecutivo, riesgos_detectados, recomendaciones_optimizacion_coste, "
        "recomendaciones_operacion, alertas_gobernanza_uso_responsable. "
        f"Datos: {json.dumps(metrica, ensure_ascii=False)}"
    )


def _categoria_http(status: int) -> str:
    if status == 401:
        return "autenticacion_401"
    if status == 403:
        return "permisos_403"
    if status == 404:
        return "endpoint_o_modelo_404"
    if status == 429:
        return "rate_limit_429"
    return "http_error"


def _extraer_mensaje_error_http(exc: error.HTTPError) -> str:
    try:
        cuerpo = exc.read().decode("utf-8", errors="replace")
        data = json.loads(cuerpo)
        return str(data.get("error", {}).get("message", "")).strip()[:240]
    except Exception:
        return ""


def analizar_con_groq(metrica: dict[str, Any], timeout: int = 12) -> dict[str, Any]:
    model = os.environ.get("GROQ_MODEL", MODELO_POR_DEFECTO).strip() or MODELO_POR_DEFECTO
    api_key = os.environ.get("GROQ_API_KEY", "").strip()
    if not api_key:
        raise GroqError(
            categoria="falta_clave",
            mensaje_seguro="No se encontró GROQ_API_KEY en el entorno.",
            modelo=model,
        )

    payload = {
        "model": model,
        "temperature": 0.1,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": "Eres un analista de observabilidad y costes de IA empresarial."},
            {"role": "user", "content": _build_prompt(metrica)},
        ],
    }

    data = json.dumps(payload).encode("utf-8")
    req = request.Request(
        GROQ_URL,
        data=data,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        },
    )

    try:
        with request.urlopen(req, timeout=timeout) as resp:
            status = getattr(resp, "status", 200)
            body = json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as exc:
        categoria = _categoria_http(exc.code)
        detalle = _extraer_mensaje_error_http(exc)
        mensaje = f"Error HTTP {exc.code} al invocar Groq."
        if detalle:
            mensaje = f"{mensaje} Detalle: {detalle}"
        raise GroqError(categoria=categoria, mensaje_seguro=mensaje, http_status=exc.code, modelo=model) from exc
    except TimeoutError as exc:
        raise GroqError(categoria="timeout_red", mensaje_seguro="Timeout de red al invocar Groq.", modelo=model) from exc
    except error.URLError as exc:
        raise GroqError(
            categoria="timeout_red",
            mensaje_seguro=f"Error de red al invocar Groq: {exc.reason}",
            modelo=model,
        ) from exc
    except json.JSONDecodeError as exc:
        raise GroqError(
            categoria="respuesta_mal_formada",
            mensaje_seguro="La respuesta HTTP de Groq no es JSON válido.",
            modelo=model,
        ) from exc
    except Exception as exc:
        raise GroqError(
            categoria="otro_error_seguro",
            mensaje_seguro=f"Error no clasificado al invocar Groq: {type(exc).__name__}",
            modelo=model,
        ) from exc

    content = body.get("choices", [{}])[0].get("message", {}).get("content", "{}")
    try:
        analisis = json.loads(content)
    except json.JSONDecodeError as exc:
        raise GroqError(
            categoria="respuesta_mal_formada",
            mensaje_seguro="El contenido de respuesta de Groq no es JSON válido.",
            http_status=status,
            modelo=model,
        ) from exc

    analisis["modo"] = "groq"
    analisis["modelo_groq"] = model
    analisis["http_status_groq"] = status
    return analisis
