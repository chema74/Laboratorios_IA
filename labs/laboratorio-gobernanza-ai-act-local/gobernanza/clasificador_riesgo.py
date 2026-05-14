def clasificar_caso(caso: dict) -> dict:
    motivos = []
    puntaje = 0

    if caso.get("criticidad") == "alta":
        puntaje += 2
        motivos.append("criticidad alta")
    if caso.get("grado_automatizacion") == "alto":
        puntaje += 2
        motivos.append("alto grado de automatización")
    if caso.get("supervision_humana") == "baja":
        puntaje += 2
        motivos.append("baja supervisión humana")
    if "sensibles" in caso.get("datos_tratados", "").lower():
        puntaje += 2
        motivos.append("tratamiento de datos sensibles")

    if puntaje <= 1:
        categoria = "riesgo mínimo"
    elif puntaje <= 3:
        categoria = "riesgo limitado"
    elif puntaje <= 5:
        categoria = "riesgo alto orientativo"
    else:
        categoria = "revisión obligatoria"

    advertencias = [
        "Clasificación heurística y orientativa.",
        "No constituye dictamen legal definitivo.",
    ]
    return {"categoria": categoria, "motivos": motivos, "advertencias": advertencias, "puntaje": puntaje}
