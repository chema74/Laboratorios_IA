def evaluar_regresion(criterios_clave: list[str], respuesta_base: str, respuesta_nueva: str) -> dict:
    base = (respuesta_base or "").lower()
    nueva = (respuesta_nueva or "").lower()
    base_hits = sum(1 for c in criterios_clave if c.lower() in base)
    nueva_hits = sum(1 for c in criterios_clave if c.lower() in nueva)

    if nueva_hits > base_hits:
        veredicto = "mejora"
    elif nueva_hits < base_hits:
        veredicto = "empeora"
    else:
        veredicto = "estable"

    return {
        "veredicto": veredicto,
        "base_cobertura": base_hits,
        "nueva_cobertura": nueva_hits,
        "delta": nueva_hits - base_hits,
    }
