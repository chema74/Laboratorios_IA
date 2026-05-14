"""Costes ficticios de revisión de privacidad para laboratorio local."""


def coste_revision(casos: int) -> dict:
    total = round(casos * 0.015, 4)
    return {"moneda": "EUR", "coste_total_simulado": total, "coste_por_caso": 0.015}
