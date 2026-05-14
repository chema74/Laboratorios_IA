from __future__ import annotations

from typing import Any


def generar_analisis_fallback(metrica: dict[str, Any]) -> dict[str, Any]:
    riesgos = []
    coste = float(metrica.get("coste_total_estimado", 0.0))
    latencia = float(metrica.get("latencia_media_ms", 0.0))
    tasa_errores = float(metrica.get("tasa_errores", 0.0))
    tokens = int(metrica.get("tokens_totales", 0))
    total = int(metrica.get("total_eventos", 0))
    riesgo_eventos = int(metrica.get("eventos_riesgo", 0))

    if coste > 0.5:
        riesgos.append("Coste por encima de umbral operativo de la muestra.")
    if latencia > 1800:
        riesgos.append("Latencia media alta en flujos analizados.")
    if tasa_errores > 0.15:
        riesgos.append("Tasa de errores elevada para operación estable.")
    if tokens > 12000:
        riesgos.append("Consumo de tokens alto, riesgo de escalado de coste.")
    if total and riesgo_eventos > 0:
        riesgos.append("Eventos marcados como riesgo alto o critico.")

    concentracion = None
    coste_por_caso = metrica.get("coste_por_caso_uso", {})
    if coste_por_caso:
        caso, valor = max(coste_por_caso.items(), key=lambda kv: kv[1])
        if coste > 0 and (float(valor) / coste) >= 0.6:
            concentracion = f"El caso '{caso}' concentra {float(valor) / coste:.0%} del coste."
            riesgos.append("Concentración de consumo en un único caso de uso.")

    if not riesgos:
        riesgos = ["Sin riesgos críticos en los umbrales definidos."]

    recomendaciones_coste = [
        "Definir topes de tokens por operación.",
        "Priorizar modelos más eficientes para tareas repetitivas.",
    ]
    recomendaciones_operacion = [
        "Revisar alertas diariamente con responsable técnico.",
        "Mantener trazabilidad por evento y equipo.",
    ]
    gobernanza = []
    if riesgo_eventos > 0:
        gobernanza.append("Activar revisión humana obligatoria en casos sensibles.")
    if tasa_errores > 0.15:
        gobernanza.append("Registrar postmortem de errores repetidos.")
    if not gobernanza:
        gobernanza.append("Gobernanza operativa dentro de umbrales de laboratorio.")

    resumen = (
        f"Se analizaron {total} eventos con coste total estimado de {coste:.4f} EUR, "
        f"latencia media de {latencia:.1f} ms y tasa de errores de {tasa_errores:.2%}."
    )

    return {
        "modo": "fallback_local",
        "resumen_ejecutivo": resumen,
        "riesgos_detectados": riesgos,
        "recomendaciones_optimizacion_coste": recomendaciones_coste,
        "recomendaciones_operacion": recomendaciones_operacion,
        "alertas_gobernanza_uso_responsable": gobernanza,
        "detalle_concentracion": concentracion,
    }
