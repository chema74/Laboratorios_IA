def obligaciones_por_riesgo(categoria: str, mapa: dict) -> list[str]:
    return mapa.get(categoria, [])
