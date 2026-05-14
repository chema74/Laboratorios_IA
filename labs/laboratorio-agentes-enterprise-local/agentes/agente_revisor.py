def revisar_resultados(ejecucion: dict) -> dict:
    completos = len(ejecucion.get("resultados", []))
    bloqueos = ejecucion.get("bloqueos", [])
    riesgos = []
    if completos < 3:
        riesgos.append("baja cobertura de pasos")
    if bloqueos:
        riesgos.append("acciones bloqueadas detectadas")
    estado = "aprobado" if completos >= 3 and not bloqueos else "con_observaciones"
    return {"estado": estado, "pasos_completos": completos, "riesgos": riesgos}
