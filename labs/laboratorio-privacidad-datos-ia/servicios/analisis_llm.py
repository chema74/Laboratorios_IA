import json
import os
from typing import Any
from urllib import request

URL_GROQ = "https://api.groq.com/openai/v1/chat/completions"
MODELO_POR_DEFECTO = "llama-3.1-8b-instant"


def _bool_env(nombre: str) -> bool:
    valor = os.getenv(nombre, "").strip().lower()
    return valor in {"1", "true", "yes", "si", "on"}


def _bool_env_en(nombre: str, entorno: dict[str, str]) -> bool:
    valor = str(entorno.get(nombre, "")).strip().lower()
    return valor in {"1", "true", "yes", "si", "on"}


def _cargar_entorno(cargar_env: bool = True) -> dict[str, str]:
    if cargar_env:
        try:
            from dotenv import load_dotenv

            load_dotenv()
        except Exception:
            pass
    return dict(os.environ)


def _compactar(resultado_motor: dict) -> dict:
    analisis = resultado_motor.get("analisis_casos", [])
    total_hallazgos = sum(len(c.get("detecciones", [])) for c in analisis)
    return {
        "casos": len(analisis),
        "riesgo": resultado_motor.get("evaluacion_exposicion", {}).get("nivel_riesgo", "desconocido"),
        "score": resultado_motor.get("evaluacion_exposicion", {}).get("puntuacion", 0),
        "hallazgos_pii": total_hallazgos,
        "salidas_estado": [v.get("estado", "desconocido") for v in resultado_motor.get("validacion_salidas", [])],
    }


def _prompt(payload: dict) -> str:
    return (
        "Eres analista de privacidad. Responde en JSON con campos: resumen, riesgos, recomendaciones. "
        "Usa frases cortas y accionables. Datos:\n" + json.dumps(payload, ensure_ascii=False)
    )


def _fallback(payload: dict, motivo: str, trazas: dict[str, Any]) -> dict:
    riesgo = payload.get("riesgo", "desconocido")
    recomendaciones = [
        "Aplicar anonimización previa a cualquier intercambio externo.",
        "Reducir campos no necesarios en prompts antes del procesamiento.",
        "Mantener validación de salida para bloquear PII de severidad alta.",
    ]
    resumen = (
        f"Fallback local activo. Casos={payload.get('casos', 0)}, "
        f"hallazgos_pii={payload.get('hallazgos_pii', 0)}, riesgo={riesgo}."
    )
    riesgos = [
        f"Nivel de riesgo detectado: {riesgo}",
        "Exposición residual posible en prompts no minimizados.",
        "Filtración en salida si no se aplica bloqueo automático.",
    ]
    return {
        "proveedor": "fallback_local",
        "modo": "determinista",
        "motivo_fallback": motivo,
        "trazabilidad": trazas,
        "respuesta": {
            "resumen": resumen,
            "riesgos": riesgos,
            "recomendaciones": recomendaciones,
        },
    }


def _llamar_groq_http(api_key: str, payload: dict, modelo: str, opener=request.urlopen) -> dict:
    cuerpo = {
        "model": modelo,
        "temperature": 0,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": "Analista técnico de privacidad de datos."},
            {"role": "user", "content": _prompt(payload)},
        ],
    }
    req = request.Request(
        URL_GROQ,
        data=json.dumps(cuerpo).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with opener(req, timeout=20) as resp:
        raw = json.loads(resp.read().decode("utf-8"))
    contenido = raw["choices"][0]["message"]["content"]
    return json.loads(contenido)


def _llamar_groq_sdk(api_key: str, payload: dict, modelo: str) -> dict:
    from groq import Groq

    cliente = Groq(api_key=api_key)
    comp = cliente.chat.completions.create(
        model=modelo,
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "Analista técnico de privacidad de datos."},
            {"role": "user", "content": _prompt(payload)},
        ],
    )
    contenido = comp.choices[0].message.content
    if not contenido:
        raise ValueError("Respuesta vacía de Groq")
    return json.loads(contenido)


def analizar_privacidad_llm(
    resultado_motor: dict,
    api_key: str | None = None,
    opener=request.urlopen,
    *,
    cargar_env: bool = True,
    entorno: dict[str, str] | None = None,
) -> dict:
    payload = _compactar(resultado_motor)
    env_actual = dict(entorno) if entorno is not None else _cargar_entorno(cargar_env=cargar_env)
    modelo = str(env_actual.get("GROQ_MODEL", MODELO_POR_DEFECTO)).strip() or MODELO_POR_DEFECTO
    opener_personalizado = opener is not request.urlopen
    trazas: dict[str, Any] = {
        "groq_api_key_activa": bool(api_key or env_actual.get("GROQ_API_KEY")),
        "forzar_fallback_local": _bool_env_en("FORZAR_FALLBACK_LOCAL", env_actual),
        "groq_model": modelo,
        "sdk_groq_disponible": False,
        "opener_personalizado": opener_personalizado,
        "ruta_ejecucion": "indefinida",
    }

    if trazas["forzar_fallback_local"]:
        trazas["ruta_ejecucion"] = "fallback_forzado"
        return _fallback(payload, "FORZAR_FALLBACK_LOCAL activa", trazas)

    clave = api_key or env_actual.get("GROQ_API_KEY")
    if not clave:
        trazas["ruta_ejecucion"] = "fallback_sin_clave"
        return _fallback(payload, "GROQ_API_KEY no configurada", trazas)

    try:
        import groq  # noqa: F401

        trazas["sdk_groq_disponible"] = True
    except Exception:
        trazas["sdk_groq_disponible"] = False

    try:
        usar_sdk = trazas["sdk_groq_disponible"] and not opener_personalizado
        if usar_sdk:
            trazas["ruta_ejecucion"] = "groq_sdk"
            respuesta = _llamar_groq_sdk(clave, payload, modelo)
        else:
            trazas["ruta_ejecucion"] = "groq_http"
            respuesta = _llamar_groq_http(clave, payload, modelo, opener=opener)
        return {
            "proveedor": "groq",
            "modo": "remoto",
            "modelo": modelo,
            "trazabilidad": trazas,
            "respuesta": respuesta,
        }
    except Exception as exc:
        detalle = str(exc).strip().replace("\n", " ")[:220]
        motivo = f"Error Groq ({type(exc).__name__}): {detalle}" if detalle else f"Error Groq: {type(exc).__name__}"
        return _fallback(payload, motivo, trazas)
