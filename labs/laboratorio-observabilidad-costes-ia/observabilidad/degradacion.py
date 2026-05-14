def detectar_degradacion(latencias: dict, errores: dict, feedback: dict, costes: dict) -> list[dict]:
    alertas = []
    if latencias.get("p95_aprox", 0) > 1400:
        alertas.append({"tipo": "latencia", "severidad": "alta", "detalle": "P95 elevado"})
    if errores.get("tasa_error", 0) >= 0.2:
        alertas.append({"tipo": "errores", "severidad": "alta", "detalle": "Tasa de error alta"})
    if feedback.get("satisfaccion_media", 0) < 3:
        alertas.append({"tipo": "feedback", "severidad": "media", "detalle": "Satisfacción baja"})
    if costes.get("coste_medio", 0) > 0.035:
        alertas.append({"tipo": "coste", "severidad": "media", "detalle": "Coste medio creciente"})
    return alertas
