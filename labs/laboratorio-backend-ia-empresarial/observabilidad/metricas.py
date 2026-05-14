def calcular_metricas(registros: list[dict], tareas_procesadas: int) -> dict:
    modulos = {}
    ok = 0
    err = 0
    for r in registros:
        m = r.get("modulo", "desconocido")
        modulos[m] = modulos.get(m, 0) + 1
        if r.get("estado") == "ok":
            ok += 1
        else:
            err += 1
    return {"total_peticiones": len(registros), "exito": ok, "error": err, "modulos_usados": modulos, "tareas_procesadas": tareas_procesadas}
