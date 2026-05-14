CAMPOS_REQUERIDOS = ["endpoint", "metodo", "payload", "usuario", "rol", "traza_id"]


def validar_peticion(peticion: dict) -> dict:
    errores = []
    for c in CAMPOS_REQUERIDOS:
        if c not in peticion:
            errores.append({"campo": c, "error": "faltante"})
    return {"valida": len(errores) == 0, "errores": errores}
