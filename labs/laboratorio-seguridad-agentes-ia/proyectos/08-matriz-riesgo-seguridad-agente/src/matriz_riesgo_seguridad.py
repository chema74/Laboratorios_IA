from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any


def cargar_json(r: Path) -> Any:
    with r.open("r", encoding="utf-8") as f:
        return json.load(f)


def score(e: dict[str, Any], cfg: dict[str, Any]) -> float:
    p = cfg["pesos_impacto"]
    s = (
        e["impacto_confidencialidad_simulado"] * p["confidencialidad"]
        + e["impacto_integridad_simulado"] * p["integridad"]
        + e["impacto_disponibilidad_simulado"] * p["disponibilidad"]
        + e["impacto_privacidad_simulado"] * p["privacidad"]
        + e["probabilidad_simulada"] * p["probabilidad"]
    )
    if e.get("detectabilidad") == "baja":
        s += 0.3
    return round(s, 2)


def nivel(s: float, cfg: dict[str, Any]) -> str:
    u = cfg["umbrales_riesgo"]
    if s >= u["alto"]:
        return "critico"
    if s >= u["medio"]:
        return "alto"
    if s >= u["bajo"]:
        return "medio"
    return "bajo"


def procesar(esc: list[dict[str, Any]], cfg: dict[str, Any]) -> dict[str, Any]:
    out = []
    err = []
    matriz = defaultdict(int)
    for e in esc:
        bad = []
        if e.get("categoria_riesgo") not in cfg["categorias_permitidas"]:
            bad.append("categoria inválida")
        if e.get("severidad_simulada") not in cfg["severidades_permitidas"]:
            bad.append("severidad inválida")
        for k in ("usa_datos_reales", "usa_ia_real", "usa_api_externa", "usa_cloud"):
            if e.get(k) is not False:
                bad.append(f"{k} debe ser false")
        if bad:
            err.append(f"{e.get('id_escenario','SIN_ID')}: " + " | ".join(bad))
            continue
        sc = score(e, cfg)
        lv = nivel(sc, cfg)
        impacto_prom = round((e["impacto_confidencialidad_simulado"] + e["impacto_integridad_simulado"] + e["impacto_disponibilidad_simulado"] + e["impacto_privacidad_simulado"]) / 4, 1)
        matriz[f"P{e['probabilidad_simulada']}-I{impacto_prom}"] += 1
        out.append({
            "id_escenario": e["id_escenario"],
            "categoria_riesgo": e["categoria_riesgo"],
            "puntuacion_riesgo": sc,
            "nivel_riesgo": lv,
            "factores_principales": [e["detectabilidad"], e["prioridad_mitigacion"]],
            "controles_recomendados": e["controles_recomendados"] or cfg["controles_defensivos_recomendados"],
            "prioridad_mitigacion": e["prioridad_mitigacion"],
            "explicacion_defensiva": "Nivel asignado por impacto, probabilidad y detectabilidad simulada.",
            "activo_simulado_afectado": e["activo_simulado_afectado"],
            "detectabilidad": e["detectabilidad"],
            "controles_existentes": e["controles_existentes"],
            "usa_datos_reales": False,
            "usa_ia_real": False,
            "usa_api_externa": False,
            "usa_cloud": False,
        })
    return {
        "fecha_generacion": datetime.now().isoformat(timespec="seconds"),
        "total_escenarios_evaluados": len(out),
        "errores_validacion": err,
        "matriz_probabilidad_x_impacto": dict(matriz),
        "distribucion_por_nivel": dict(Counter(x["nivel_riesgo"] for x in out)),
        "riesgos_criticos": [x for x in out if x["nivel_riesgo"] == "critico"],
        "riesgos_por_categoria": dict(Counter(x["categoria_riesgo"] for x in out)),
        "riesgos_por_activo": dict(Counter(x["activo_simulado_afectado"] for x in out)),
        "riesgos_baja_detectabilidad": [x for x in out if x["detectabilidad"] == "baja"],
        "riesgos_controles_insuficientes": [x for x in out if len(x["controles_existentes"]) < 1],
        "controles_defensivos_recomendados": cfg["controles_defensivos_recomendados"],
        "resultados": out,
    }


def md(r: dict[str, Any]) -> str:
    lines = [
        "# Informe de Matriz de Riesgo de Seguridad del Agente",
        "",
        f"Fecha de generación: {r['fecha_generacion']}",
        "",
        "## Resumen ejecutivo",
        "Evaluación local de escenarios sintéticos para priorizar mitigaciones defensivas.",
        "",
        "## Total de escenarios evaluados",
        str(r["total_escenarios_evaluados"]),
        "",
        "## Matriz probabilidad x impacto",
    ]
    lines += [f"- {k}: {v}" for k, v in r["matriz_probabilidad_x_impacto"].items()]
    lines += ["", "## Distribución por nivel de riesgo"]
    lines += [f"- {k}: {v}" for k, v in r["distribucion_por_nivel"].items()]
    lines += ["", "## Riesgos críticos"]
    lines += [f"- {x['id_escenario']} ({x['categoria_riesgo']})" for x in r["riesgos_criticos"]] or ["- Ninguno"]
    lines += ["", "## Riesgos por categoría"]
    lines += [f"- {k}: {v}" for k, v in r["riesgos_por_categoria"].items()]
    lines += ["", "## Riesgos por activo simulado"]
    lines += [f"- {k}: {v}" for k, v in r["riesgos_por_activo"].items()]
    lines += ["", "## Riesgos con controles insuficientes"]
    lines += [f"- {x['id_escenario']}" for x in r["riesgos_controles_insuficientes"]] or ["- Ninguno"]
    lines += ["", "## Controles defensivos recomendados"]
    lines += [f"- {x}" for x in r["controles_defensivos_recomendados"]]
    lines += [
        "",
        "## Lectura técnica defensiva",
        "Se priorizan escenarios críticos y de baja detectabilidad para mitigación temprana.",
        "",
        "## Límites de la matriz",
        "Solo datos sintéticos y reglas locales; no representa entorno productivo.",
        "",
        "## Recomendaciones siguientes",
        "1. Reforzar controles en riesgos críticos.",
        "2. Mejorar detectabilidad en escenarios ambiguos.",
        "3. Integrar resultados con trazabilidad de incidentes.",
        "",
        "## 🪪 Licencia y Autoría",
        "Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  ",
        "© 2025 – Txema Ríos. Todos los derechos compartidos.",
    ]
    return "\n".join(lines) + "\n"


def ejecutar(sc: Path, cfg: Path, out_md: Path, out_json: Path) -> dict[str, Any]:
    r = procesar(cargar_json(sc), cargar_json(cfg))
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(md(r), encoding="utf-8")
    out_json.write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")
    return r


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--scenarios", required=True, type=Path)
    p.add_argument("--config", required=True, type=Path)
    p.add_argument("--output-md", required=True, type=Path)
    p.add_argument("--output-json", required=True, type=Path)
    a = p.parse_args()
    r = ejecutar(a.scenarios, a.config, a.output_md, a.output_json)
    print(f"Matriz generada. Escenarios válidos: {r['total_escenarios_evaluados']}")


if __name__ == "__main__":
    main()
