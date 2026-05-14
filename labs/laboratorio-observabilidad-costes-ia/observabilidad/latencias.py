def analizar_latencias(eventos: list[dict], umbral_lento_ms: int = 1200) -> dict:
    lats = sorted([int(e["latencia_ms"]) for e in eventos])
    if not lats:
        return {"media": 0, "min": 0, "max": 0, "p95_aprox": 0, "lentos": []}
    n = len(lats)
    idx95 = min(n - 1, int(round(0.95 * (n - 1))))
    media = sum(lats) / n
    lentos = [e for e in eventos if int(e["latencia_ms"]) >= umbral_lento_ms]
    return {
        "media": round(media, 2),
        "min": lats[0],
        "max": lats[-1],
        "p95_aprox": lats[idx95],
        "lentos": lentos,
    }
