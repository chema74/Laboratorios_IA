def evaluar_exposicion(total_pii: int, severidades: list[str], en_prompt: int, en_salida: int, no_minimizados: int) -> dict:
    score = total_pii + en_prompt + (2 * en_salida) + no_minimizados
    score += sum(1 for s in severidades if s == "alta")

    if score <= 2:
        nivel = "bajo"
    elif score <= 5:
        nivel = "medio"
    elif score <= 8:
        nivel = "alto"
    else:
        nivel = "critico"

    recs = [
        "Aplicar anonimización previa al procesamiento.",
        "Minimizar campos no esenciales en prompts.",
        "Bloquear salidas con PII de severidad alta.",
    ]
    return {"puntuacion": score, "nivel_riesgo": nivel, "recomendaciones": recs}
