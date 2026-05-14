def evaluar_trazabilidad(resultado: dict) -> dict:
    trazas = resultado.get("trazas", [])
    memoria = resultado.get("memoria", [])
    suficiente = len(trazas) >= 3 and len(memoria) >= 3
    return {"trazas": len(trazas), "memoria": len(memoria), "suficiente": suficiente}
