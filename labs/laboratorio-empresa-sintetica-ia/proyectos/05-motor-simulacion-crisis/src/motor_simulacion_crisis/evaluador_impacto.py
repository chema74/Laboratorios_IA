"""Construcción de resumen e informe de impacto simulado."""

from __future__ import annotations

from collections import Counter


def construir_resumen_crisis(crisis: list[dict], linea_tiempo: list[dict], entradas_utilizadas: dict[str, str]) -> dict:
    por_tipo = Counter(x["tipo_crisis"] for x in crisis)
    por_severidad = Counter(x["severidad"] for x in crisis)
    revisiones = sum(1 for x in crisis if x.get("requiere_revision_humana"))

    areas = Counter()
    riesgos = Counter()
    decisiones = Counter()

    for c in crisis:
        for a in c.get("areas_afectadas", "").split(","):
            if a:
                areas[a] += 1
        for r in c.get("riesgos_secundarios", "").split(","):
            if r:
                riesgos[r] += 1
        for d in c.get("decisiones_recomendadas", "").split(","):
            if d:
                decisiones[d] += 1

    return {
        "total_crisis": len(crisis),
        "crisis_por_tipo": dict(por_tipo),
        "crisis_por_severidad": dict(por_severidad),
        "crisis_que_requieren_revision_humana": revisiones,
        "areas_mas_afectadas": dict(areas),
        "riesgos_secundarios_detectados": dict(riesgos),
        "decisiones_recomendadas": dict(decisiones),
        "entradas_utilizadas": entradas_utilizadas,
        "advertencia_sobre_datos_sinteticos": "Crisis simuladas sobre datos sintéticos. No representan hechos reales.",
        "advertencia_sobre_no_uso_operativo_real": "No usar este resultado para operación real ni predicción empresarial.",
        "hitos_linea_tiempo": len(linea_tiempo),
    }


def construir_expediente_markdown(crisis: list[dict], linea_tiempo: list[dict], resumen: dict) -> str:
    lista_crisis = "\n".join(
        [f"- {c['id_crisis']} | {c['tipo_crisis']} | severidad={c['severidad']} | estado={c['estado_crisis']}" for c in crisis]
    )
    hitos = "\n".join(
        [f"- {h['fecha']} | {h['id_crisis']} | {h['tipo_hito']} | decision={h['decision_pendiente']}" for h in linea_tiempo[:15]]
    )

    return (
        "# Expediente de Crisis Simuladas\n\n"
        "**Aviso:** Simulación sintética para pruebas internas del laboratorio. No corresponde a una empresa real.\n\n"
        "## Resumen ejecutivo ficticio\n"
        f"Se han simulado {resumen['total_crisis']} crisis con {resumen['hitos_linea_tiempo']} hitos temporales.\n\n"
        "## Crisis simuladas\n"
        f"{lista_crisis}\n\n"
        "## Línea temporal resumida\n"
        f"{hitos}\n\n"
        "## Impacto estimado\n"
        "Impacto estimado ficticio sobre ingresos, operaciones, pagos pendientes y alertas.\n\n"
        "## Recomendaciones simuladas\n"
        "Aplicar revisión de datos, escalar a humano y activar contingencia simulada según severidad.\n\n"
        "## Límites de uso\n"
        "- No usar para toma de decisiones reales.\n"
        "- No ejecutar acciones automáticas reales.\n"
        "- No constituye análisis empresarial real.\n"
        "- No constituye predicción real.\n\n"
        "## Nota final\n"
        "Este expediente no representa una evaluación operativa real ni un diagnóstico empresarial real.\n"
    )
