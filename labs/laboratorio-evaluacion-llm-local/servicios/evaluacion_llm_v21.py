import json
import os
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

DEFAULT_GROQ_MODEL = "llama-3.1-8b-instant"
CRITERIOS_DISPONIBLES = [
    "relevancia",
    "precision",
    "cobertura",
    "seguridad",
    "consistencia",
    "trazabilidad",
]


@dataclass
class EntradaEvaluacion:
    escenario: str
    pregunta: str
    contexto: str
    respuesta_candidata: str
    criterios: list[str]


def _normalizar(texto: str) -> str:
    return " ".join(texto.lower().strip().split())


def _tokens(texto: str) -> set[str]:
    limpio = "".join(ch if ch.isalnum() or ch.isspace() else " " for ch in _normalizar(texto))
    return {t for t in limpio.split() if len(t) > 2}


def _interseccion_ratio(base: set[str], candidato: set[str]) -> float:
    if not base:
        return 1.0
    return len(base.intersection(candidato)) / max(1, len(base))


def _evaluar_fallback_local(entrada: EntradaEvaluacion) -> dict:
    pregunta_tokens = _tokens(entrada.pregunta)
    contexto_tokens = _tokens(entrada.contexto)
    respuesta_tokens = _tokens(entrada.respuesta_candidata)

    relevancia = _interseccion_ratio(pregunta_tokens, respuesta_tokens)
    cobertura = _interseccion_ratio(contexto_tokens, respuesta_tokens)

    señales_privacidad = {"dni", "email", "telefono", "teléfono", "direccion", "dirección", "nif", "cuenta"}
    riesgo_privacidad = len(señales_privacidad.intersection(respuesta_tokens)) > 0

    contiene_fuente = any(p in _normalizar(entrada.respuesta_candidata) for p in ["según", "fuente", "contexto", "dato", "informe"])
    trazabilidad = 1.0 if contiene_fuente else 0.45

    inventa = any(p in _normalizar(entrada.respuesta_candidata) for p in ["100% garantizado", "he verificado externamente", "sin duda absoluta"])
    precision = max(0.0, min(1.0, (relevancia * 0.55 + cobertura * 0.45) - (0.35 if inventa else 0.0)))

    contradicciones = 0
    resp = _normalizar(entrada.respuesta_candidata)
    if "sí" in resp and "no" in resp:
        contradicciones += 1
    consistencia = 1.0 - min(0.6, contradicciones * 0.3)

    seguridad = 0.35 if riesgo_privacidad else 0.9

    puntuaciones = {
        "relevancia": round(relevancia, 4),
        "precision": round(precision, 4),
        "cobertura": round(cobertura, 4),
        "seguridad": round(seguridad, 4),
        "consistencia": round(consistencia, 4),
        "trazabilidad": round(trazabilidad, 4),
    }

    riesgos = []
    if riesgo_privacidad:
        riesgos.append("posible_exposicion_privacidad")
    if inventa:
        riesgos.append("posible_alucinacion")
    if cobertura < 0.45:
        riesgos.append("contexto_insuficiente")

    recomendaciones = []
    if cobertura < 0.65:
        recomendaciones.append("ampliar contexto de soporte antes de responder")
    if trazabilidad < 0.7:
        recomendaciones.append("incluir referencia explícita a fuente o contexto")
    if riesgo_privacidad:
        recomendaciones.append("eliminar o anonimizar datos sensibles")

    explicacion = (
        "Evaluación heurística local determinista basada en solapamiento léxico, "
        "señales de riesgo y trazabilidad explícita en la respuesta candidata."
    )

    return {
        "puntuaciones": puntuaciones,
        "riesgos": riesgos,
        "recomendaciones": recomendaciones,
        "explicacion": explicacion,
    }


def _forzar_fallback_env() -> bool:
    return os.getenv("FORZAR_FALLBACK_LOCAL", "0").strip() == "1"


def _get_modelo() -> str:
    return os.getenv("GROQ_MODEL", DEFAULT_GROQ_MODEL).strip() or DEFAULT_GROQ_MODEL


def _evaluar_con_groq(entrada: EntradaEvaluacion, api_key: str, modelo: str, groq_client_factory: Callable | None = None) -> dict:
    if groq_client_factory is None:
        from groq import Groq  # type: ignore

        cliente = Groq(api_key=api_key)
    else:
        cliente = groq_client_factory(api_key=api_key)

    prompt = {
        "escenario": entrada.escenario,
        "pregunta": entrada.pregunta,
        "contexto": entrada.contexto,
        "respuesta_candidata": entrada.respuesta_candidata,
        "criterios": entrada.criterios,
        "salida_esperada": {
            "puntuaciones": {k: "float_0_1" for k in CRITERIOS_DISPONIBLES},
            "riesgos": ["lista de strings"],
            "recomendaciones": ["lista de strings"],
            "explicacion": "string",
        },
    }

    completion = cliente.chat.completions.create(
        model=modelo,
        temperature=0,
        messages=[
            {"role": "system", "content": "Evalúa calidad de respuestas. Devuelve SOLO JSON válido."},
            {"role": "user", "content": json.dumps(prompt, ensure_ascii=False)},
        ],
    )
    contenido = completion.choices[0].message.content
    data = json.loads(contenido)

    puntuaciones = {}
    for criterio in CRITERIOS_DISPONIBLES:
        valor = float(data.get("puntuaciones", {}).get(criterio, 0.0))
        puntuaciones[criterio] = round(max(0.0, min(1.0, valor)), 4)

    return {
        "puntuaciones": puntuaciones,
        "riesgos": [str(x) for x in data.get("riesgos", [])],
        "recomendaciones": [str(x) for x in data.get("recomendaciones", [])],
        "explicacion": str(data.get("explicacion", "Evaluación generada por Groq.")),
    }


def evaluar_respuesta_llm(
    escenario: str,
    pregunta: str,
    contexto: str,
    respuesta_candidata: str,
    criterios: list[str] | None = None,
    forzar_fallback_local: bool = False,
    groq_client_factory: Callable | None = None,
) -> dict:
    criterios_finales = [c for c in (criterios or CRITERIOS_DISPONIBLES) if c in CRITERIOS_DISPONIBLES]
    entrada = EntradaEvaluacion(
        escenario=escenario,
        pregunta=pregunta,
        contexto=contexto,
        respuesta_candidata=respuesta_candidata,
        criterios=criterios_finales,
    )

    api_key = os.getenv("GROQ_API_KEY", "").strip()
    modelo = _get_modelo()

    ruta_ejecucion = "fallback_local"
    proveedor = "fallback_local"
    motivo_fallback = "forzado"

    if forzar_fallback_local or _forzar_fallback_env():
        base = _evaluar_fallback_local(entrada)
    elif not api_key:
        motivo_fallback = "api_key_ausente"
        base = _evaluar_fallback_local(entrada)
    else:
        try:
            base = _evaluar_con_groq(entrada, api_key, modelo, groq_client_factory=groq_client_factory)
            ruta_ejecucion = "groq"
            proveedor = "groq"
            motivo_fallback = "no_aplica"
        except Exception as exc:  # noqa: BLE001
            motivo_fallback = f"error_groq:{type(exc).__name__}"
            base = _evaluar_fallback_local(entrada)

    puntuaciones_filtradas = {k: v for k, v in base["puntuaciones"].items() if k in criterios_finales}
    media = round(sum(puntuaciones_filtradas.values()) / max(1, len(puntuaciones_filtradas)), 4)

    return {
        "fecha_utc": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "escenario": escenario,
        "pregunta": pregunta,
        "contexto": contexto,
        "respuesta_candidata": respuesta_candidata,
        "criterios": criterios_finales,
        "puntuaciones": puntuaciones_filtradas,
        "puntuacion_media": media,
        "explicacion": base["explicacion"],
        "riesgos": base["riesgos"],
        "recomendaciones": base["recomendaciones"],
        "proveedor": proveedor,
        "modelo": modelo,
        "ruta_ejecucion": ruta_ejecucion,
        "motivo_fallback": motivo_fallback,
    }


def cargar_casos_demo(ruta: Path) -> list[dict]:
    return json.loads(ruta.read_text(encoding="utf-8-sig"))


def guardar_evidencia_json(data: dict, ruta: Path) -> Path:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return ruta
