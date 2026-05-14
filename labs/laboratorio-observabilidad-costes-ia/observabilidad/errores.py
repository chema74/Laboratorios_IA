def analizar_errores(eventos: list[dict]) -> dict:
    total = len(eventos)
    errores = [e for e in eventos if e.get("estado") == "error"]
    por_tipo = {}
    por_caso = {}
    for e in errores:
        t = e.get("tipo_error", "desconocido")
        por_tipo[t] = por_tipo.get(t, 0) + 1
        c = e.get("caso_uso")
        por_caso[c] = por_caso.get(c, 0) + 1
    top_casos = sorted(por_caso.items(), key=lambda x: x[1], reverse=True)
    return {"tasa_error": round(len(errores) / max(total, 1), 4), "errores_total": len(errores), "errores_por_tipo": por_tipo, "casos_mas_incidencias": top_casos[:3]}
