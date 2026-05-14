def aplicar_politicas_retencion(riesgo: str) -> list[str]:
    acciones = ["conservar evidencia técnica", "eliminar contexto sensible", "seudonimizar identificadores"]
    if riesgo in {"alto", "critico"}:
        acciones.append("revisar salidas con riesgo")
    return acciones
