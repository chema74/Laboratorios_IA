from privacidad.detector_pii import detectar_pii

REEMPLAZOS = {
    "nombre": "[NOMBRE]",
    "email": "[EMAIL]",
    "telefono": "[TELEFONO]",
    "identificador": "[IDENTIFICADOR]",
    "direccion": "[DIRECCION]",
}


def anonimizar_texto(texto: str, nombres_marcados: list[str] | None = None) -> dict:
    out = texto or ""
    hallazgos = detectar_pii(out, nombres_marcados=nombres_marcados)
    cambios = []
    for h in hallazgos:
        marcador = REEMPLAZOS.get(h["tipo"], "[DATO]")
        if h["valor"] in out:
            out = out.replace(h["valor"], marcador)
            cambios.append({"tipo": h["tipo"], "original": h["valor"], "nuevo": marcador})
    return {"texto_anonimizado": out, "cambios": cambios}
