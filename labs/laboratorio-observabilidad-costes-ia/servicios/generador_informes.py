from pathlib import Path


def generar_informe(resultado: dict, ruta: Path) -> Path:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    r = resultado
    lineas = [
        "# Informe Observabilidad y Costes IA",
        "",
        "## Resumen ejecutivo",
        f"- Eventos analizados: {r['resumen_eventos']['total']}",
        f"- Coste total simulado: {r['costes']['coste_total']} {r['costes']['moneda']}",
        f"- Latencia P95 aprox: {r['latencias']['p95_aprox']} ms",
        f"- Tasa de error: {r['errores']['tasa_error']}",
        f"- Satisfacción media: {r['feedback']['satisfaccion_media']}",
        f"- Estado presupuesto: {r['presupuesto']['estado']}",
        "",
        "## Alertas de degradación",
    ]
    for a in r["alertas_degradacion"]:
        lineas.append(f"- {a['tipo']} ({a['severidad']}): {a['detalle']}")
    if not r["alertas_degradacion"]:
        lineas.append("- Sin alertas")

    lineas.extend([
        "",
        "## Recomendaciones técnicas",
        "- Reducir latencia de operaciones por encima del P95 objetivo.",
        "- Revisar flujos con mayor tasa de error por caso de uso.",
        "- Ajustar presupuesto operativo según tendencia de coste simulado.",
    ])
    ruta.write_text("\n".join(lineas), encoding="utf-8")
    return ruta
