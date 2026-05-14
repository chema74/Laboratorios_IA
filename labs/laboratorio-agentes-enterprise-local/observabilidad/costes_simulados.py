"""Costes ficticios de laboratorio, no equivalen a precios reales."""


def coste_ejecucion(resultado: dict) -> dict:
    pasos = len(resultado.get("ejecucion", {}).get("resultados", []))
    bloqueos = len(resultado.get("ejecucion", {}).get("bloqueos", []))
    total = round(0.005 * pasos + 0.001 * bloqueos, 4)
    return {"coste_total_simulado_eur": total, "moneda": "EUR", "detalle": {"pasos": pasos, "bloqueos": bloqueos}}
