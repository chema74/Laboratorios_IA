"""Costes ficticios de laboratorio, orientativos y no vinculados a proveedores reales."""


def coste_revision(total_casos: int) -> dict:
    total = round(0.02 * total_casos, 4)
    return {"coste_total_simulado_eur": total, "coste_por_caso_eur": 0.02, "moneda": "EUR"}
