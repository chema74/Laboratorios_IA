def validar_salida_con_citas(salida: dict) -> tuple[bool, str]:
    respuesta = (salida or {}).get("respuesta", "").strip()
    citas = (salida or {}).get("citas", [])
    if not respuesta:
        return False, "respuesta vacía"
    if not citas:
        return False, "respuesta sin citas"
    return True, "ok"
