CAMPOS_MINIMOS = ["responsable", "descripcion_funcional", "datos_tratados", "revision_humana", "trazabilidad", "politica_interna"]


def validar_evidencias(caso_id: str, evidencias: dict) -> dict:
    registro = evidencias.get(caso_id, {})
    faltantes = [c for c in CAMPOS_MINIMOS if not registro.get(c)]
    return {"caso_id": caso_id, "completo": len(faltantes) == 0, "faltantes": faltantes}
