def analizar_shadow_ia(items: list[dict]) -> list[dict]:
    salida = []
    for i in items:
        if not i.get("declarado", False) or i.get("documentacion", "baja") == "baja":
            sev = "alta" if i.get("impacto", "medio") == "alto" else "media"
            salida.append({
                "id": i["id"],
                "severidad": sev,
                "recomendacion": "Regularizar en inventario y asignar responsable.",
            })
    return salida
