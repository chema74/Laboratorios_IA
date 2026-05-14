from pathlib import Path


def generar_informe(resultado: dict, ruta_informe: Path, ruta_fichas: Path) -> tuple[Path, list[Path]]:
    ruta_informe.parent.mkdir(parents=True, exist_ok=True)
    ruta_fichas.mkdir(parents=True, exist_ok=True)

    r = resultado
    lineas = [
        "# Informe Gobernanza AI Act (Orientativo)",
        "",
        "## Aviso",
        "Este informe es técnico y orientativo. No constituye asesoramiento legal definitivo.",
        "",
        "## Resumen ejecutivo",
        f"- Casos inventariados: {r['resumen_inventario']['total']}",
        f"- Alertas shadow IA: {len(r['shadow_ia'])}",
        f"- Casos con evidencias faltantes: {len(r['evidencias_faltantes'])}",
        f"- Coste simulado de revisión: {r['coste_simulado']['coste_total_simulado_eur']} EUR",
        "",
        "## Recomendaciones",
        "- Regularizar usos no declarados en inventario.",
        "- Completar evidencias mínimas por caso de uso.",
        "- Ejecutar revisión periódica de casos con riesgo alto orientativo.",
    ]
    ruta_informe.write_text("\n".join(lineas), encoding="utf-8")

    rutas = []
    for ficha in r["fichas"]:
        rf = ruta_fichas / f"ficha_{ficha['id']}.md"
        rf.write_text(ficha["contenido"], encoding="utf-8")
        rutas.append(rf)
    return ruta_informe, rutas
