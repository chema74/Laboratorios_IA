from pathlib import Path


def generar_informe(resultado: dict, ruta: Path) -> Path:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    r = resultado
    lineas = [
        "# Informe Privacidad de Datos en IA",
        "",
        "## Aviso",
        "Comprobaciones técnicas, heurísticas y orientativas. No constituye asesoramiento legal definitivo.",
        "",
        "## Resumen ejecutivo",
        f"- Casos analizados: {len(r['analisis_casos'])}",
        f"- Riesgo de exposición: {r['evaluacion_exposicion']['nivel_riesgo']} (score={r['evaluacion_exposicion']['puntuacion']})",
        f"- Coste simulado: {r['coste_simulado']['coste_total_simulado']} {r['coste_simulado']['moneda']}",
        "",
        "## Validación de salidas",
    ]
    for i, v in enumerate(r["validacion_salidas"], start=1):
        lineas.append(f"- Salida {i}: {v['estado']} | hallazgos={len(v['hallazgos'])}")

    lineas.extend([
        "",
        "## Recomendaciones",
        "- Anonimizar o seudonimizar antes de procesar texto sensible.",
        "- Aplicar minimización estricta de contexto en prompts.",
        "- Bloquear salidas con PII de severidad alta.",
    ])
    ruta.write_text("\n".join(lineas), encoding="utf-8")
    return ruta
