def registrar_eventos(eventos: list[dict]) -> dict:
    return {"total": len(eventos), "eventos": eventos}


def filtrar_eventos(eventos: list[dict], caso_uso: str | None = None, estado: str | None = None, riesgo: str | None = None) -> list[dict]:
    salida = eventos
    if caso_uso:
        salida = [e for e in salida if e.get("caso_uso") == caso_uso]
    if estado:
        salida = [e for e in salida if e.get("estado") == estado]
    if riesgo:
        salida = [e for e in salida if e.get("riesgo") == riesgo]
    return salida


def resumir_eventos(eventos: list[dict]) -> dict:
    por_estado = {}
    for e in eventos:
        por_estado[e["estado"]] = por_estado.get(e["estado"], 0) + 1
    return {"total": len(eventos), "por_estado": por_estado}
