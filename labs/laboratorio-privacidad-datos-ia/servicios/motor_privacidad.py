import json

from app.config import RUTA_DATASET, RUTA_POLITICAS, RUTA_PROMPTS, RUTA_REGISTRO, RUTA_SALIDAS
from observabilidad.costes_simulados import coste_revision
from observabilidad.trazas import Traza
from privacidad.anonimizador import anonimizar_texto
from privacidad.detector_pii import detectar_pii
from privacidad.evaluador_exposicion import evaluar_exposicion
from privacidad.minimizador_contexto import minimizar_contexto
from privacidad.politicas_retencion import aplicar_politicas_retencion
from privacidad.registro_tratamiento import resumir_tratamiento
from privacidad.seudonimizador import seudonimizar_texto
from privacidad.validador_salida import validar_salida


def _load(path):
    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def ejecutar_motor() -> dict:
    tr = Traza()
    dataset = _load(RUTA_DATASET)
    politicas = _load(RUTA_POLITICAS)
    prompts = _load(RUTA_PROMPTS)
    salidas = _load(RUTA_SALIDAS)
    registro = _load(RUTA_REGISTRO)
    tr.registrar("carga_datos", {"casos": len(dataset)})

    analisis = []
    total_pii = 0
    severidades = []

    for caso in dataset:
        nombres = caso.get("nombres_marcados", [])
        texto = caso["texto"]
        det = detectar_pii(texto, nombres_marcados=nombres)
        total_pii += len(det)
        severidades.extend([d["severidad"] for d in det])
        anon = anonimizar_texto(texto, nombres_marcados=nombres)
        seud = seudonimizar_texto(texto, nombres_marcados=nombres)
        analisis.append({"id": caso["id"], "detecciones": det, "anonimizacion": anon, "seudonimizacion": seud})

    prompts_min = [minimizar_contexto(p) for p in prompts]
    validaciones = [validar_salida(s["salida"]) for s in salidas]
    en_prompt = sum(1 for p in prompts for _ in detectar_pii(p.get("texto", "")))
    en_salida = sum(1 for s in salidas for _ in detectar_pii(s.get("salida", "")))
    no_min = sum(1 for p in prompts if any(k in p for k in ["email", "telefono", "direccion"]))

    expos = evaluar_exposicion(total_pii, severidades, en_prompt, en_salida, no_min)
    acciones_ret = aplicar_politicas_retencion(expos["nivel_riesgo"])
    reg = resumir_tratamiento(registro, acciones_ret, ["informe_privacidad_datos_ia.md"])
    coste = coste_revision(len(dataset))
    tr.registrar("analisis", {"pii": total_pii, "riesgo": expos["nivel_riesgo"]})

    return {
        "analisis_casos": analisis,
        "prompts_minimizados": prompts_min,
        "validacion_salidas": validaciones,
        "evaluacion_exposicion": expos,
        "politicas": politicas,
        "registro_tratamiento": reg,
        "coste_simulado": coste,
        "trazas": tr.eventos,
    }
