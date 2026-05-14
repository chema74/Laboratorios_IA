from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from statistics import mean
from typing import Any


def cargar_json(r: Path) -> Any:
    with r.open("r", encoding="utf-8") as f:
        return json.load(f)


def nivel_madurez(score: float, umb: dict[str, float]) -> str:
    if score >= umb["intermedia"]:
        return "alta"
    if score >= umb["basica"]:
        return "intermedia"
    if score >= umb["inicial"]:
        return "basica"
    return "inicial"


def evaluar(res: dict[str, Any], cfg: dict[str, Any]) -> dict[str, Any]:
    dimensiones = cfg["dimensiones_evaluacion"]
    pesos = cfg["pesos_dimension"]
    por_dimension = {}
    for d in dimensiones:
        por_dimension[d] = float(res[d]["puntuacion"])
    weighted = sum(por_dimension[d] * pesos[d] for d in dimensiones)
    score_global = round((weighted + mean(por_dimension.values())) / 2, 2)
    madurez = nivel_madurez(score_global, cfg["umbrales_madurez_defensiva"])

    riesgos = []
    if res["inventario_riesgos"]["riesgos_criticos"] > 0:
        riesgos.append("riesgos_criticos_inventario")
    if res["matriz_riesgo"]["criticos"] > 0:
        riesgos.append("riesgos_criticos_matriz")
    if res["trazabilidad_incidentes"]["trazabilidad_debil"] > 0:
        riesgos.append("trazabilidad_debil")

    controles = res["controles_aplicados"]
    faltantes = [c for c in cfg["controles_minimos_recomendados"] if c not in controles]

    decision = "no_apto_uso_real"
    if madurez == "alta" and not faltantes:
        decision = "apto_con_controles"

    return {
        "metadatos": {"fecha_generacion": datetime.now().isoformat(timespec="seconds"), "modo": "local-simulado-defensivo"},
        "puntuacion_global": score_global,
        "nivel_madurez": madurez,
        "resultados_por_dimension": por_dimension,
        "riesgos_principales": riesgos,
        "controles": {"existentes": controles, "faltantes": faltantes},
        "brechas": faltantes,
        "incidentes_relevantes": ["trazabilidad_debil"] if res["trazabilidad_incidentes"]["trazabilidad_debil"] > 0 else [],
        "politicas_activadas": ["P-002", "P-006", "P-007"],
        "herramientas_bloqueadas": ["exportador_datos_simulado"],
        "sensibilidad_detectada": "alta",
        "trazabilidad_defensiva": "parcial" if res["trazabilidad_incidentes"]["trazabilidad_debil"] > 0 else "fuerte",
        "recomendaciones": res["recomendaciones_defensivas"],
        "decision_defensiva_recomendada": decision,
        "limites_declarados": cfg["nota_alcance"],
    }


def md(rep: dict[str, Any]) -> str:
    lines = [
        "# Informe Defensivo Consolidado de Seguridad de Agente",
        "",
        f"Fecha de generación: {rep['metadatos']['fecha_generacion']}",
        "",
        "## Resumen ejecutivo",
        "Consolidación local de evidencias sintéticas del laboratorio defensivo.",
        "",
        f"## Puntuación global defensiva\n{rep['puntuacion_global']}",
        "",
        f"## Nivel de madurez defensiva\n{rep['nivel_madurez']}",
        "",
        "## Lectura por dimensión",
    ]
    lines += [f"- {k}: {v}" for k, v in rep["resultados_por_dimension"].items()]
    lines += ["", "## Riesgos principales"]
    lines += [f"- {x}" for x in rep["riesgos_principales"]] or ["- Ninguno"]
    lines += ["", "## Controles defensivos aplicados"]
    lines += [f"- {x}" for x in rep["controles"]["existentes"]]
    lines += ["", "## Brechas defensivas simuladas"]
    lines += [f"- {x}" for x in rep["brechas"]] or ["- Ninguna"]
    lines += ["", "## Incidentes simulados relevantes"]
    lines += [f"- {x}" for x in rep["incidentes_relevantes"]] or ["- Ninguno"]
    lines += [
        "",
        f"## Decisión defensiva recomendada\n{rep['decision_defensiva_recomendada']}",
        "",
        "## Condiciones mínimas antes de uso real",
        "- Mantener revisión humana obligatoria.",
        "- Cerrar brechas de controles mínimos.",
        "- Garantizar trazabilidad completa.",
        "",
        "## Límites del análisis",
        rep["limites_declarados"],
        "",
        "## Recomendaciones siguientes",
    ]
    lines += [f"- {x}" for x in rep["recomendaciones"]]
    lines += [
        "",
        "## 🪪 Licencia y Autoría",
        "Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  ",
        "© 2025 – Txema Ríos. Todos los derechos compartidos.",
    ]
    return "\n".join(lines) + "\n"


def ejecutar(results: Path, config: Path, out_md: Path, out_json: Path) -> dict[str, Any]:
    rep = evaluar(cargar_json(results), cargar_json(config))
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(md(rep), encoding="utf-8")
    out_json.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
    return rep


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--results", required=True, type=Path)
    p.add_argument("--config", required=True, type=Path)
    p.add_argument("--output-md", required=True, type=Path)
    p.add_argument("--output-json", required=True, type=Path)
    a = p.parse_args()
    r = ejecutar(a.results, a.config, a.output_md, a.output_json)
    print(f"Informe defensivo generado. Madurez: {r['nivel_madurez']}")


if __name__ == "__main__":
    main()
