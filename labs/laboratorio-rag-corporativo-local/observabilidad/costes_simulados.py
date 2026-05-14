def estimar_coste_simulado(consulta: str, resultados: int) -> dict:
    chars = len((consulta or ""))
    coste = round(0.00002 * chars + 0.0003 * resultados, 6)
    return {
        "moneda": "EUR",
        "coste_estimado": coste,
        "detalle": {
            "chars_consulta": chars,
            "resultados": resultados,
            "modelo": "simulado_local_v1",
        },
    }
