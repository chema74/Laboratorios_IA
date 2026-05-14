def analizar_feedback(items: list[dict]) -> dict:
    if not items:
        return {"satisfaccion_media": 0.0, "negativos": [], "por_caso": {}}
    media = sum(float(i["satisfaccion"]) for i in items) / len(items)
    negativos = [i for i in items if float(i["satisfaccion"]) <= 2]
    por_caso = {}
    for i in items:
        c = i["caso_uso"]
        por_caso.setdefault(c, []).append(float(i["satisfaccion"]))
    por_caso_media = {k: round(sum(v) / len(v), 2) for k, v in por_caso.items()}
    return {"satisfaccion_media": round(media, 2), "negativos": negativos, "por_caso": por_caso_media}
