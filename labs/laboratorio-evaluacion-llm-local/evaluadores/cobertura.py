def evaluar_cobertura(criterios_clave: list[str], respuesta_candidata: str) -> dict:
    texto = (respuesta_candidata or "").lower()
    cubiertos = [c for c in criterios_clave if c.lower() in texto]
    no_cubiertos = [c for c in criterios_clave if c.lower() not in texto]
    total = max(len(criterios_clave), 1)
    score = len(cubiertos) / total
    return {
        "puntuacion": round(score, 4),
        "cubiertos": cubiertos,
        "no_cubiertos": no_cubiertos,
    }
