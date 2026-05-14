from privacidad.detector_pii import detectar_pii


def seudonimizar_texto(texto: str, nombres_marcados: list[str] | None = None) -> dict:
    hallazgos = detectar_pii(texto, nombres_marcados=nombres_marcados)
    mapa = {}
    contadores = {"nombre": 0, "email": 0, "telefono": 0, "identificador": 0, "direccion": 0}
    out = texto or ""

    for h in hallazgos:
        clave = (h["tipo"], h["valor"])
        if clave not in mapa:
            contadores[h["tipo"]] += 1
            mapa[clave] = f"{h['tipo']}_{contadores[h['tipo']]:03d}"
        out = out.replace(h["valor"], mapa[clave])

    correspondencia = {f"{k[0]}::{k[1]}": v for k, v in mapa.items()}
    return {"texto_seudonimizado": out, "correspondencia": correspondencia}
