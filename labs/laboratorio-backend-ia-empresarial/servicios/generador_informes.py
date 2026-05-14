from pathlib import Path


def generar_informe(ruta: Path, resumen: dict) -> Path:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    lineas = [
        "# Informe Backend IA Empresarial",
        "",
        "## Resumen ejecutivo",
        f"- Total peticiones: {resumen['metricas']['total_peticiones']}",
        f"- Éxitos: {resumen['metricas']['exito']}",
        f"- Errores: {resumen['metricas']['error']}",
        f"- Tareas procesadas: {resumen['metricas']['tareas_procesadas']}",
        f"- Coste simulado: {resumen['coste']['coste_total_simulado']} {resumen['coste']['moneda']}",
        "",
        "## Recomendaciones técnicas",
        "- Mantener contratos de petición obligatorios por endpoint.",
        "- Revisar permisos por rol antes de desplegar integración real.",
        "- Consolidar auditoría como requisito de operación backend.",
    ]
    ruta.write_text("\n".join(lineas), encoding="utf-8")
    return ruta
