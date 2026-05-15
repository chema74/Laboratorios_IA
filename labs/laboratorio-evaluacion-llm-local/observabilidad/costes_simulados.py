def coste_por_caso(texto: str) -> float:
    return round(0.00001 * len(texto or "") + 0.0005, 6)


def coste_total(casos: list[dict]) -> dict:
    total = round(sum(coste_por_caso(c.get("respuesta", "")) for c in casos), 6)
    return {"moneda": "EUR", "coste_total": total, "modelo": "simulado_eval_v1"}
