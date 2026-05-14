def evaluar_presupuesto(coste_total: float, presupuesto_mensual: float) -> dict:
    ratio = coste_total / max(presupuesto_mensual, 0.000001)
    if ratio < 0.8:
        estado = "correcto"
    elif ratio <= 1.0:
        estado = "vigilancia"
    else:
        estado = "excedido"
    return {"estado": estado, "ratio": round(ratio, 4), "coste_total": coste_total, "presupuesto_mensual": presupuesto_mensual}
