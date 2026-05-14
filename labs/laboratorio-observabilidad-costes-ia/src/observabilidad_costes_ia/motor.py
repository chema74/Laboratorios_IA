from __future__ import annotations

from collections import Counter, defaultdict
from statistics import mean
from typing import Any

from .modelos import normalizar_evento


def _top_contador(valores: list[str]) -> dict[str, int]:
    return dict(Counter(valores).most_common(3))


def analizar_eventos(eventos: list[dict[str, Any]]) -> dict[str, Any]:
    normalizados = [normalizar_evento(ev, idx + 1) for idx, ev in enumerate(eventos)]
    total = len(normalizados)
    if total == 0:
        return {
            "total_eventos": 0,
            "coste_total_estimado": 0.0,
            "coste_por_caso_uso": {},
            "tokens_totales": 0,
            "latencia_media_ms": 0.0,
            "tasa_errores": 0.0,
            "eventos_riesgo": 0,
            "proveedores_mas_usados": {},
            "modelos_mas_usados": {},
            "alertas": [],
            "recomendaciones_operativas": ["Sin eventos para analizar."],
            "eventos": [],
        }

    coste_total = sum(ev["coste_estimado_eur"] for ev in normalizados)
    tokens_totales = sum(ev["tokens_entrada"] + ev["tokens_salida"] for ev in normalizados)
    latencia_media = mean(ev["latencia_ms"] for ev in normalizados)
    errores = sum(1 for ev in normalizados if str(ev["estado"]).lower() != "ok")
    tasa_errores = errores / total
    eventos_riesgo = sum(1 for ev in normalizados if str(ev["riesgo"]).lower() in {"alto", "critico", "crítico"})

    coste_por_caso = defaultdict(float)
    uso_por_caso = defaultdict(int)
    for ev in normalizados:
        caso = str(ev["caso_uso"])
        coste_por_caso[caso] += float(ev["coste_estimado_eur"])
        uso_por_caso[caso] += 1

    alertas: list[dict[str, str]] = []
    recomendaciones: list[str] = []

    if coste_total > 0.5:
        alertas.append({"tipo": "coste_alto", "severidad": "alta", "detalle": "El coste total supera 0.50 EUR en la muestra."})
        recomendaciones.append("Aplicar límites de tokens por solicitud y revisar prompts largos.")

    if latencia_media > 1800:
        alertas.append({"tipo": "latencia_alta", "severidad": "alta", "detalle": "La latencia media supera 1800 ms."})
        recomendaciones.append("Priorizar colas, caché de respuestas y modelos más rápidos para flujos críticos.")

    if tasa_errores > 0.15:
        alertas.append({"tipo": "errores", "severidad": "alta", "detalle": "La tasa de errores supera el 15%."})
        recomendaciones.append("Añadir reintentos controlados y observabilidad de errores por caso de uso.")

    if tokens_totales > 12000:
        alertas.append({"tipo": "exceso_tokens", "severidad": "media", "detalle": "El volumen total de tokens supera 12000."})
        recomendaciones.append("Reducir contexto, usar plantillas compactas y resumir historiales.")

    caso_top, uso_top = max(uso_por_caso.items(), key=lambda item: item[1])
    if uso_top / total >= 0.6:
        alertas.append({"tipo": "concentracion_uso", "severidad": "media", "detalle": f"El caso '{caso_top}' concentra el {uso_top / total:.0%} del uso."})
        recomendaciones.append("Diversificar pruebas y revisar capacidad del equipo para el caso dominante.")

    if eventos_riesgo > 0:
        alertas.append({"tipo": "riesgo", "severidad": "alta", "detalle": "Se detectan eventos de riesgo alto/critico."})
        recomendaciones.append("Aplicar revisión humana y trazabilidad reforzada en casos sensibles.")

    if not recomendaciones:
        recomendaciones.append("Operación estable en la muestra. Mantener monitorización diaria.")

    return {
        "total_eventos": total,
        "coste_total_estimado": round(coste_total, 6),
        "coste_por_caso_uso": {k: round(v, 6) for k, v in sorted(coste_por_caso.items())},
        "tokens_totales": tokens_totales,
        "latencia_media_ms": round(latencia_media, 2),
        "tasa_errores": round(tasa_errores, 4),
        "eventos_riesgo": eventos_riesgo,
        "proveedores_mas_usados": _top_contador([str(ev["proveedor"]) for ev in normalizados]),
        "modelos_mas_usados": _top_contador([str(ev["modelo"]) for ev in normalizados]),
        "alertas": alertas,
        "recomendaciones_operativas": recomendaciones,
        "eventos": normalizados,
    }
