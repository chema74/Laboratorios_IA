import json


def cargar_casos(path) -> list[dict]:
    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def filtrar_casos(casos: list[dict], area: str | None = None, criticidad: str | None = None, automatizacion: str | None = None) -> list[dict]:
    out = casos
    if area:
        out = [c for c in out if c["area"] == area]
    if criticidad:
        out = [c for c in out if c["criticidad"] == criticidad]
    if automatizacion:
        out = [c for c in out if c["grado_automatizacion"] == automatizacion]
    return out


def resumir_inventario(casos: list[dict]) -> dict:
    por_area = {}
    for c in casos:
        por_area[c["area"]] = por_area.get(c["area"], 0) + 1
    return {"total": len(casos), "por_area": por_area}
