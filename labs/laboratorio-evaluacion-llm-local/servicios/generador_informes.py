from pathlib import Path


def generar_informe_markdown(resultado: dict, destino: Path) -> Path:
    destino.parent.mkdir(parents=True, exist_ok=True)
    m = resultado["metricas"]
    lineas = [
        "# Informe de Evaluación LLM Local V1",
        "",
        "## Resumen ejecutivo",
        f"- Total respuestas evaluadas: {m['total_respuestas']}",
        f"- Media puntuación total: {m['media_puntuacion_total']}",
        f"- Casos con riesgo de alucinación: {m['casos_riesgo']}",
        f"- Coste simulado total: {m['coste_simulado']['coste_total']} {m['coste_simulado']['moneda']}",
        "",
        "## Casos aprobados",
    ]

    aprobados = [e for e in resultado["evaluaciones"] if e["puntuacion_total"] >= 0.7]
    for a in aprobados:
        lineas.append(f"- {a['caso_id']} / {a['respuesta_id']} -> {a['puntuacion_total']}")

    lineas.append("")
    lineas.append("## Casos con riesgo")
    riesgos = [e for e in resultado["evaluaciones"] if e["alucinaciones"]["riesgo"] > 0]
    for r in riesgos:
        lineas.append(f"- {r['caso_id']} / {r['respuesta_id']} -> alertas={r['alucinaciones']['alertas']}")

    lineas.append("")
    lineas.append("## Regresiones detectadas")
    for reg in resultado["regresiones"]:
        lineas.append(f"- {reg['caso_id']}: {reg['veredicto']} (delta={reg['delta']})")

    lineas.append("")
    lineas.append("## Recomendaciones técnicas")
    lineas.extend([
        "- Reforzar prompts en casos con cobertura parcial de criterios clave.",
        "- Evitar cifras no respaldadas por la referencia esperada.",
        "- Exigir trazabilidad explícita en formato 'según política/procedimiento'.",
    ])

    destino.write_text("\n".join(lineas), encoding="utf-8")
    return destino
