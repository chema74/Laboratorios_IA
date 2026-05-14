def generar_ficha_markdown(caso: dict, clasificacion: dict, evidencias: dict) -> str:
    return "\n".join([
        f"# Ficha Sistema IA - {caso['identificador']}",
        f"- Nombre: {caso['nombre']}",
        f"- Área: {caso['area']}",
        f"- Propósito: {caso['descripcion']}",
        f"- Datos tratados: {caso['datos_tratados']}",
        f"- Riesgo orientativo: {clasificacion['categoria']}",
        f"- Supervisión humana: {caso['supervision_humana']}",
        f"- Evidencias completas: {evidencias['completo']}",
        "- Límites: clasificación heurística, sin valor de dictamen legal.",
    ])
