"""Costes ficticios de laboratorio. No representan precios reales de proveedores."""


def analizar_costes(eventos: list[dict]) -> dict:
    total = round(sum(float(e["coste_simulado_eur"]) for e in eventos), 6)
    media = round(total / max(len(eventos), 1), 6)
    por_caso = {}
    for e in eventos:
        caso = e["caso_uso"]
        por_caso[caso] = round(por_caso.get(caso, 0.0) + float(e["coste_simulado_eur"]), 6)
    return {"coste_total": total, "coste_medio": media, "coste_por_caso": por_caso, "moneda": "EUR"}
