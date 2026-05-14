def cargar_politicas(politicas: list[dict]) -> dict:
    return {p["accion"]: p["permitida"] for p in politicas}
