def construir_respuesta(estado: str, codigo: str, mensaje: str, datos: dict, trazabilidad: dict) -> dict:
    return {
        "estado": estado,
        "codigo_interno": codigo,
        "mensaje": mensaje,
        "datos": datos,
        "trazabilidad": trazabilidad,
    }
