def ejecutar_job(tipo: str, payload: dict) -> dict:
    if tipo == "revision_privacidad":
        return {"resultado": "ok", "detalle": "revisión sintética completada", "traza": payload.get("traza_id")}
    if tipo == "evaluacion_respuesta":
        return {"resultado": "ok", "detalle": "evaluación sintética completada", "traza": payload.get("traza_id")}
    if tipo == "consulta_documental":
        return {"resultado": "ok", "detalle": "consulta documental sintética completada", "traza": payload.get("traza_id")}
    return {"resultado": "error", "detalle": "job no soportado", "traza": payload.get("traza_id")}
