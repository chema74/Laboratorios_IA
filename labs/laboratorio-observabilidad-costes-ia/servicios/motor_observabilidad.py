import json

from app.config import RUTA_EVENTOS, RUTA_FEEDBACK, RUTA_PRESUPUESTO
from observabilidad.costes_simulados import analizar_costes
from observabilidad.degradacion import detectar_degradacion
from observabilidad.errores import analizar_errores
from observabilidad.feedback import analizar_feedback
from observabilidad.latencias import analizar_latencias
from observabilidad.presupuesto import evaluar_presupuesto
from observabilidad.trazador import registrar_eventos, resumir_eventos

from servicios.simulador_eventos import enriquecer_eventos


def _load(path):
    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def ejecutar_motor_observabilidad() -> dict:
    eventos = enriquecer_eventos(_load(RUTA_EVENTOS))
    presupuesto = _load(RUTA_PRESUPUESTO)
    feedback = _load(RUTA_FEEDBACK)

    traza = registrar_eventos(eventos)
    resumen = resumir_eventos(eventos)
    lat = analizar_latencias(eventos)
    costes = analizar_costes(eventos)
    errs = analizar_errores(eventos)
    fb = analizar_feedback(feedback)
    pres = evaluar_presupuesto(costes["coste_total"], float(presupuesto["presupuesto_mensual_eur"]))
    alertas = detectar_degradacion(lat, errs, fb, costes)

    return {
        "resumen_eventos": resumen,
        "latencias": lat,
        "costes": costes,
        "errores": errs,
        "feedback": fb,
        "presupuesto": pres,
        "alertas_degradacion": alertas,
        "trazas": {"total_eventos_registrados": traza["total"]},
    }
