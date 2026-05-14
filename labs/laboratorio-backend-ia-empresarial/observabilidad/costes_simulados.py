"""Costes ficticios de operación backend local."""


def estimar_coste(operaciones: int) -> dict:
    total = round(operaciones * 0.01, 4)
    return {"moneda": "EUR", "coste_total_simulado": total, "coste_unitario": 0.01}
