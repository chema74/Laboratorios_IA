def ordenar_respuestas(resultados: list[dict]) -> list[dict]:
    ordenado = sorted(resultados, key=lambda r: r.get("puntuacion_total", 0), reverse=True)
    for i, r in enumerate(ordenado, start=1):
        r["clasificacion"] = f"puesto_{i}"
        r["explicacion_clasificacion"] = f"Ordenada por puntuación total={r.get('puntuacion_total', 0):.4f}"
    return ordenado
