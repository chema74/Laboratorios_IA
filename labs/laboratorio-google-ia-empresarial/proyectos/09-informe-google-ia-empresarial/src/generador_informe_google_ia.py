"""Generador local de informe consolidado Google IA empresarial simulado."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from statistics import mean


def cargar_json(ruta: Path) -> dict:
    with ruta.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def nivel_madurez(score: float, umbrales: dict) -> str:
    if score >= umbrales["alto"]:
        return "alto"
    if score >= umbrales["intermedio"]:
        return "intermedio"
    if score >= umbrales["basico"]:
        return "básico"
    return "inicial"


def construir_resultado(results: dict, config: dict) -> dict:
    modulos = results["modulos"]
    valores = [v["valor"] for v in modulos.values()]
    global_score = round(mean(valores), 2)
    madurez = nivel_madurez(global_score, config["umbrales_madurez"])
    fortalezas = [v["fortaleza"] for v in modulos.values()][:5]
    riesgos = [v["riesgo"] for v in modulos.values()][:5]
    brechas = [r for r in results["riesgos_y_limites"] if "sin_" in r]
    por_dimension = {
        "arquitectura": modulos["01_mapa_ecosistema"]["valor"],
        "automatizacion": round(mean([modulos["02_gmail_simulado"]["valor"], modulos["05_calendar_tareas"]["valor"], modulos["06_gemini_fallback"]["valor"]]), 2),
        "analitica": modulos["04_sheets"]["valor"],
        "gobierno": modulos["07_gobierno_permisos"]["valor"],
        "trazabilidad": modulos["08_trazabilidad"]["valor"],
        "resiliencia": modulos["06_gemini_fallback"]["valor"],
    }
    mejor_preparados = sorted(modulos.keys(), key=lambda k: modulos[k]["valor"], reverse=True)[:3]
    revision_futura = sorted(modulos.keys(), key=lambda k: modulos[k]["valor"])[:3]
    recomendaciones = list(results["recomendaciones_empresariales"]) + config["controles_minimos_recomendados"]
    return {
        "metadatos": {"fecha_generacion": datetime.now().isoformat(timespec="seconds"), "modo": "local-simulado"},
        "puntuacion_global": global_score,
        "nivel_madurez": madurez,
        "resultados_por_dimension": por_dimension,
        "fortalezas": fortalezas,
        "riesgos": riesgos,
        "brechas": brechas,
        "recomendaciones": recomendaciones,
        "oportunidades_automatizacion": ["orquestacion_cross_modulo", "reglas_alerta_avanzadas", "trazabilidad_extendida"],
        "modulos_mejor_preparados": mejor_preparados,
        "modulos_revision_futura": revision_futura,
        "decision_recomendada_v1": "continuar_v1_local_con_controles",
        "recomendaciones_v2_opcional": config["posibles_extensiones_v2"],
        "limites_declarados": results["riesgos_y_limites"],
    }


def generar_md(resultado: dict, out_md: Path) -> None:
    l = [
        "# Informe Google IA Empresarial Simulado",
        "",
        f"**Fecha de generación:** {resultado['metadatos']['fecha_generacion']}",
        "",
        "## Resumen ejecutivo",
        "Consolidación local del laboratorio Google IA empresarial con evaluación de madurez y recomendaciones.",
        "",
        "## Puntuación global simulada",
        f"- {resultado['puntuacion_global']}",
        "",
        "## Nivel de madurez",
        f"- {resultado['nivel_madurez']}",
        "",
        "## Lectura por dimensión",
    ]
    for k, v in resultado["resultados_por_dimension"].items():
        l.append(f"- {k}: {v}")
    l.extend(
        [
            "",
            "## Mapa de capacidades Google simuladas",
            "- Gmail/Drive/Docs/Sheets/Calendar en modo local simulado.",
            "",
            "## Automatizaciones empresariales simuladas",
            "- Reglas sintéticas y fallback local sin red.",
            "",
            "## Gobierno y permisos",
            "- Decisiones de mantener/revisar/reducir/revocar en entorno ficticio.",
            "",
            "## Trazabilidad",
            "- Trazas con hash simulado y evidencia local.",
            "",
            "## Riesgos principales",
        ]
    )
    for r in resultado["riesgos"]:
        l.append(f"- {r}")
    l.extend(["", "## Brechas y límites"])
    for b in resultado["brechas"]:
        l.append(f"- {b}")
    l.extend(
        [
            "",
            "## Decisión recomendada",
            f"- {resultado['decision_recomendada_v1']}",
            "",
            "## Condiciones mínimas antes de una integración real",
            "- Mantener controles de permisos, trazabilidad y fallback local.",
            "",
            "## Posibles extensiones V2 con .env y fallback local",
        ]
    )
    for v2 in resultado["recomendaciones_v2_opcional"]:
        l.append(f"- {v2}")
    l.extend(["", "## Recomendaciones siguientes"])
    for rec in resultado["recomendaciones"][:8]:
        l.append(f"- {rec}")
    l.extend(
        [
            "",
            "## 🪪 Licencia y Autoría",
            "Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  ",
            "© 2025 – Txema Ríos. Todos los derechos compartidos.",
        ]
    )
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text("\n".join(l), encoding="utf-8")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--results", required=True)
    p.add_argument("--config", required=True)
    p.add_argument("--output-md", required=True)
    p.add_argument("--output-json", required=True)
    a = p.parse_args()
    r = cargar_json(Path(a.results))
    c = cargar_json(Path(a.config))
    out = construir_resultado(r, c)
    out_json = Path(a.output_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    generar_md(out, Path(a.output_md))


if __name__ == "__main__":
    main()
