from privacidad.detector_pii import detectar_pii


def validar_salida(texto: str) -> dict:
    hallazgos = detectar_pii(texto)
    if not hallazgos:
        estado = "segura"
    elif any(h["severidad"] == "alta" for h in hallazgos):
        estado = "bloquear"
    else:
        estado = "revisar"
    return {"estado": estado, "hallazgos": hallazgos}
