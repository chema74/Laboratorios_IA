import json
import os
from typing import Any
from urllib import request

URL_GROQ = "https://api.groq.com/openai/v1/chat/completions"
MODELO_POR_DEFECTO = "llama-3.1-8b-instant"
_CAMPOS_TEXTO_FRAGMENTO = ("texto", "contenido", "fragmento", "documento", "titulo", "referencia")


def _bool_env_en(nombre: str, entorno: dict[str, str]) -> bool:
    valor = str(entorno.get(nombre, "")).strip().lower()
    return valor in {"1", "true", "yes", "si", "on"}


def _a_texto_seguro(valor: Any) -> str:
    if isinstance(valor, str):
        return valor
    try:
        return json.dumps(valor, ensure_ascii=False)
    except Exception:
        return str(valor)


def _fragmento_a_texto(fragmento: Any) -> str:
    if isinstance(fragmento, str):
        return fragmento

    if isinstance(fragmento, dict):
        for campo in _CAMPOS_TEXTO_FRAGMENTO:
            candidato = fragmento.get(campo)
            if isinstance(candidato, str) and candidato.strip():
                return candidato.strip()
            if isinstance(candidato, (dict, list)):
                serializado = _a_texto_seguro(candidato).strip()
                if serializado:
                    return serializado
        return _a_texto_seguro(fragmento)

    return _a_texto_seguro(fragmento)


def _normalizar_fragmentos_para_prompt(fragmentos: list[Any]) -> list[str]:
    normalizados: list[str] = []
    for i, fragmento in enumerate(fragmentos, start=1):
        texto = _fragmento_a_texto(fragmento).strip()
        if texto:
            normalizados.append(f"[{i}] {texto}")
    return normalizados


def _prompt(consulta: str, fragmentos: list[Any]) -> str:
    fragmentos_texto = _normalizar_fragmentos_para_prompt(fragmentos)
    bloque_fragmentos = "\n".join(fragmentos_texto) if fragmentos_texto else "Sin fragmentos recuperados."
    return (
        "Eres analista corporativo. Responde en JSON con campos: resumen, riesgos, recomendaciones. "
        "Usa solo evidencia de los fragmentos. "
        f"Consulta: {consulta}. Fragmentos:\n{bloque_fragmentos}"
    )


def _fallback_local(consulta: str, fragmentos: list[Any], motivo: str, trazas: dict[str, Any]) -> dict:
    if fragmentos:
        top = fragmentos[:2]
        partes: list[str] = []
        for f in top:
            if isinstance(f, dict):
                titulo = _a_texto_seguro(f.get("titulo", "sin titulo"))
                contenido = _fragmento_a_texto(f)[:120]
                partes.append(f"{titulo}: {contenido}")
            else:
                partes.append(_fragmento_a_texto(f)[:120])
        resumen_base = " | ".join(partes)
    else:
        resumen_base = "No hay fragmentos relevantes en el corpus local."

    riesgos = [
        "Interpretación incompleta si los documentos recuperados no cubren toda la consulta.",
        "Dependencia de la calidad del corpus sintético y su actualización.",
    ]
    recomendaciones = [
        "Validar respuesta con las citas antes de difundirla.",
        "Ampliar corpus con políticas faltantes para mejorar cobertura.",
        "Mantener revisión humana para decisiones de cumplimiento.",
    ]
    return {
        "proveedor": "fallback_local",
        "modo": "determinista",
        "motivo_fallback": motivo,
        "trazabilidad": trazas,
        "respuesta": {
            "resumen": f"Fallback local para '{consulta}'. Evidencia: {resumen_base}",
            "riesgos": riesgos,
            "recomendaciones": recomendaciones,
        },
    }


def _llamar_groq_http(api_key: str, consulta: str, fragmentos: list[Any], modelo: str, opener=request.urlopen) -> dict:
    cuerpo = {
        "model": modelo,
        "temperature": 0,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": "Analista técnico de cumplimiento corporativo."},
            {"role": "user", "content": _prompt(consulta, fragmentos)},
        ],
    }
    req = request.Request(
        URL_GROQ,
        data=json.dumps(cuerpo).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    with opener(req, timeout=20) as resp:
        raw = json.loads(resp.read().decode("utf-8"))
    contenido = raw["choices"][0]["message"]["content"]
    return json.loads(contenido)


def _llamar_groq_sdk(api_key: str, consulta: str, fragmentos: list[Any], modelo: str) -> dict:
    from groq import Groq

    cliente = Groq(api_key=api_key)
    comp = cliente.chat.completions.create(
        model=modelo,
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "Analista técnico de cumplimiento corporativo."},
            {"role": "user", "content": _prompt(consulta, fragmentos)},
        ],
    )
    contenido = comp.choices[0].message.content
    if not contenido:
        raise ValueError("Respuesta vacía de Groq")
    return json.loads(contenido)


def analizar_rag_llm(
    consulta: str,
    fragmentos: list[Any],
    api_key: str | None = None,
    opener=request.urlopen,
    *,
    cargar_env: bool = True,
    entorno: dict[str, str] | None = None,
) -> dict:
    env_actual = dict(entorno) if entorno is not None else dict(os.environ)
    if cargar_env:
        try:
            from dotenv import load_dotenv

            load_dotenv()
            env_actual = dict(os.environ)
        except Exception:
            pass

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
        return _fallback_local(consulta, fragmentos, "FORZAR_FALLBACK_LOCAL activa", trazas)

    clave = api_key or env_actual.get("GROQ_API_KEY")
    if not clave:
        trazas["ruta_ejecucion"] = "fallback_sin_clave"
        return _fallback_local(consulta, fragmentos, "GROQ_API_KEY no configurada", trazas)

    try:
        import groq  # noqa: F401

        trazas["sdk_groq_disponible"] = True
    except Exception:
        trazas["sdk_groq_disponible"] = False

    try:
        usar_sdk = trazas["sdk_groq_disponible"] and not opener_personalizado
        if usar_sdk:
            trazas["ruta_ejecucion"] = "groq_sdk"
            respuesta = _llamar_groq_sdk(clave, consulta, fragmentos, modelo)
        else:
            trazas["ruta_ejecucion"] = "groq_http"
            respuesta = _llamar_groq_http(clave, consulta, fragmentos, modelo, opener=opener)
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
        return _fallback_local(consulta, fragmentos, motivo, trazas)
