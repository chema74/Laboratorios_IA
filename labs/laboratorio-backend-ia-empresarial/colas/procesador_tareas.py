from colas.jobs_locales import ejecutar_job


def procesar_pendientes(cola) -> dict:
    completadas = []
    fallidas = []
    for t in list(cola.pendientes()):
        r = ejecutar_job(t.get("tipo"), t)
        if r["resultado"] == "ok":
            cola.marcar_completada(t["id"])
            completadas.append({"id": t["id"], "resultado": r})
        else:
            fallidas.append({"id": t["id"], "resultado": r})
    return {"completadas": completadas, "fallidas": fallidas, "pendientes": cola.pendientes()}
