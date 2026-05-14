import json
from statistics import mean

from app.config import RUTA_DATASET, RUTA_PROMPTS, RUTA_RESPUESTAS
from evaluadores.alucinaciones_sinteticas import evaluar_alucinaciones
from evaluadores.comparador_respuestas import ordenar_respuestas
from evaluadores.consistencia import evaluar_consistencia
from evaluadores.cobertura import evaluar_cobertura
from evaluadores.regresion_prompts import evaluar_regresion
from evaluadores.rubricas import puntuar_rubricas
from observabilidad.costes_simulados import coste_total
from observabilidad.trazas import Traza


def _cargar_json(path):
    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def ejecutar_motor() -> dict:
    traza = Traza()
    dataset = _cargar_json(RUTA_DATASET)
    respuestas = _cargar_json(RUTA_RESPUESTAS)
    prompts = _cargar_json(RUTA_PROMPTS)
    traza.registrar("carga_datos", {"casos": len(dataset), "respuestas": len(respuestas)})

    por_caso: dict[str, list[dict]] = {}
    for r in respuestas:
        por_caso.setdefault(r["caso_id"], []).append(r)

    evaluaciones = []
    regresiones = []
    for caso in dataset:
        candidatos = por_caso.get(caso["id"], [])
        resultados_caso = []
        for cand in candidatos:
            cons = evaluar_consistencia(caso["respuesta_esperada"], cand["respuesta"])
            cob = evaluar_cobertura(caso["criterios_clave"], cand["respuesta"])
            alu = evaluar_alucinaciones(caso["respuesta_esperada"], cand["respuesta"])
            claridad = 1.0 if len(cand["respuesta"].split(".")) <= 4 else 0.7
            trazabilidad = 1.0 if "según" in cand["respuesta"].lower() else 0.6
            precision = max(0.0, cons["puntuacion"] - (alu["riesgo"] * 0.5))
            ausencia_invencion = max(0.0, 1 - alu["riesgo"])
            rub = puntuar_rubricas(cons["puntuacion"], cob["puntuacion"], claridad, trazabilidad, ausencia_invencion, precision)
            total = round(mean(rub.values()), 4)
            resultados_caso.append({
                "caso_id": caso["id"],
                "respuesta_id": cand["respuesta_id"],
                "modelo_sintetico": cand["modelo_sintetico"],
                "puntuacion_total": total,
                "rubricas": rub,
                "consistencia": cons,
                "cobertura": cob,
                "alucinaciones": alu,
                "respuesta": cand["respuesta"],
            })

        ranking = ordenar_respuestas(resultados_caso)
        evaluaciones.extend(ranking)

        versiones = [p for p in prompts if p["caso_id"] == caso["id"]]
        if len(versiones) >= 2:
            base, nueva = versiones[0], versiones[1]
            reg = evaluar_regresion(caso["criterios_clave"], base["respuesta_sintetica"], nueva["respuesta_sintetica"])
            regresiones.append({"caso_id": caso["id"], **reg})

    agregadas = {
        "total_respuestas": len(evaluaciones),
        "media_puntuacion_total": round(mean([e["puntuacion_total"] for e in evaluaciones]) if evaluaciones else 0.0, 4),
        "casos_riesgo": sum(1 for e in evaluaciones if e["alucinaciones"]["riesgo"] > 0),
        "coste_simulado": coste_total(evaluaciones),
    }
    traza.registrar("metricas", agregadas)

    return {
        "evaluaciones": evaluaciones,
        "regresiones": regresiones,
        "metricas": agregadas,
        "trazas": traza.eventos,
    }
