def evaluar_resultado(resultado: dict) -> dict:
    pasos = len(resultado.get("ejecucion", {}).get("resultados", []))
    bloqueos = len(resultado.get("ejecucion", {}).get("bloqueos", []))
    resuelto = pasos >= 3
    limites_respetados = bloqueos >= 0
    score = round((0.6 if resuelto else 0.2) + (0.4 if limites_respetados else 0.0), 2)
    return {"resuelto": resuelto, "pasos_completos": pasos, "bloqueos": bloqueos, "limites_respetados": limites_respetados, "score": score}
