import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from statistics import mean


def cargar_json(ruta: Path) -> dict:
    with ruta.open("r", encoding="utf-8") as f:
        return json.load(f)


def validar_datos(data: dict, config: dict) -> None:
    modulos = data.get("modulos_resultados", [])
    if not modulos:
        raise ValueError("No hay módulos en resultados.")
    dims = set(config["dimensiones_evaluacion"])
    for m in modulos:
        if m["dimension"] not in dims:
            raise ValueError(f"Dimension no permitida: {m['modulo']}")
        for b in [
            "usa_microsoft_real",
            "usa_microsoft_graph_real",
            "usa_oauth_real",
            "usa_api_externa",
            "usa_azure",
            "usa_ia_real",
            "usa_datos_reales",
        ]:
            if m[b] is not False:
                raise ValueError(f"{m['modulo']} incumple politica en {b}")


def calcular_puntuacion_y_madurez(modulos: list[dict], config: dict) -> tuple[float, str, dict]:
    por_dim = defaultdict(list)
    for m in modulos:
        por_dim[m["dimension"]].append(m["puntuacion_simulada"])
    resultados_dim = {}
    pesos = config["pesos_dimension"]
    score = 0.0
    for dim, vals in por_dim.items():
        prom = mean(vals)
        resultados_dim[dim] = round(prom, 2)
        score += prom * float(pesos.get(dim, 0.0))
    score = round(score, 2)
    um = config["umbrales_madurez"]
    if score >= um["alto"]:
        nivel = "alto"
    elif score >= um["intermedio"]:
        nivel = "intermedio"
    elif score >= um["basico"]:
        nivel = "básico"
    else:
        nivel = "inicial"
    return score, nivel, resultados_dim


def consolidar_listas(modulos: list[dict], clave: str, top: int = 6) -> list[str]:
    c = Counter()
    for m in modulos:
        for item in m.get(clave, []):
            c[item] += 1
    return [k for k, _ in c.most_common(top)]


def decidir_v1_v2(score: float, config: dict) -> tuple[str, list[str]]:
    c = config["criterios_decision"]
    decision = "Consolidar V1 documental sin expansión funcional."
    if score >= c["v2_opcional_minimo"]:
        decision = "V1 robusta; habilitar planificación de V2 opcional con .env y fallback local."
    elif score >= c["v1_recomendada_minimo"]:
        decision = "V1 válida para portfolio técnico; continuar endurecimiento de controles."
    return decision, config["posibles_extensiones_v2"]


def generar_informe_md(res: dict) -> str:
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    md = [
        "# Informe Microsoft IA Empresarial (Consolidado V1 Local)",
        "",
        f"Fecha de generación: {fecha}",
        "",
        "## Resumen ejecutivo",
        res["decision_recomendada_v1"],
        "",
        "## Puntuación global simulada",
        f"- {res['puntuacion_global_simulada']}",
        "",
        "## Nivel de madurez",
        f"- {res['nivel_madurez_simulado']}",
        "",
        "## Lectura por dimensión",
    ]
    for k in sorted(res["resultados_por_dimension"]):
        md.append(f"- {k}: {res['resultados_por_dimension'][k]}")
    md.extend(
        [
            "",
            "## Mapa de capacidades Microsoft simuladas",
            "- Arquitectura, operación, documental, analítica, colaboración, asistencia, gobierno y trazabilidad evaluadas en local.",
            "",
            "## Automatizaciones empresariales simuladas",
            "- Flujos de clasificación, resúmenes, alertas, tareas y fallback conceptual sin integración real.",
            "",
            "## Gobierno y permisos",
            "- Aplicación de mínimo privilegio con decisiones mantener/revisar/reducir/revocar.",
            "",
            "## Trazabilidad",
            "- Generación de ID de traza y hash simulado por automatización.",
            "",
            "## Riesgos principales",
        ]
    )
    for r in res["riesgos_principales"]:
        md.append(f"- {r}")
    md.extend(["", "## Brechas y límites"])
    for b in res["brechas_simuladas"]:
        md.append(f"- {b}")
    md.extend(
        [
            "",
            "## Decisión recomendada",
            f"- {res['decision_recomendada_v1']}",
            "",
            "## Condiciones mínimas antes de una integración real",
        ]
    )
    for c in res["controles_recomendados"]:
        md.append(f"- {c}")
    md.extend(["", "## Posibles extensiones V2 con .env y fallback local"])
    for e in res["recomendaciones_v2_opcional"]:
        md.append(f"- {e}")
    md.extend(["", "## Recomendaciones siguientes"])
    for r in res["recomendaciones_siguientes"]:
        md.append(f"- {r}")
    md.extend(
        [
            "",
            "## 🪪 Licencia y Autoría",
            "Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  ",
            "© 2025 – Txema Ríos. Todos los derechos compartidos.",
            "",
        ]
    )
    return "\n".join(md)


def ejecutar(results_path: Path, config_path: Path, output_md: Path, output_json: Path) -> dict:
    data = cargar_json(results_path)
    cfg = cargar_json(config_path)
    validar_datos(data, cfg)
    modulos = data["modulos_resultados"]

    score, nivel, por_dim = calcular_puntuacion_y_madurez(modulos, cfg)
    fortalezas = consolidar_listas(modulos, "fortalezas")
    riesgos = consolidar_listas(modulos, "riesgos")
    brechas = consolidar_listas(modulos, "brechas")
    recomendaciones = consolidar_listas(modulos, "recomendaciones")
    decision, v2 = decidir_v1_v2(score, cfg)

    preparados = [m["modulo"] for m in modulos if m["puntuacion_simulada"] >= 80]
    revision = [m["modulo"] for m in modulos if m["puntuacion_simulada"] < 78]

    res = {
        "metadatos": {
            "fecha_generacion": datetime.now().isoformat(timespec="seconds"),
            "total_modulos": len(modulos),
            "nota": cfg["nota"],
        },
        "puntuacion_global_simulada": score,
        "nivel_madurez_simulado": nivel,
        "resultados_por_dimension": por_dim,
        "fortalezas_principales": fortalezas,
        "riesgos_principales": riesgos + data.get("riesgos_y_limites", []),
        "brechas_simuladas": brechas,
        "controles_recomendados": cfg["controles_minimos_recomendados"],
        "oportunidades_automatizacion": ["orquestacion_reglas", "alertas_prioridad", "seguimiento_revision"],
        "modulos_mejor_preparados": preparados,
        "modulos_requieren_revision_futura": revision,
        "decision_recomendada_v1": decision,
        "recomendaciones_v2_opcional": v2,
        "recomendaciones_siguientes": recomendaciones + data.get("recomendaciones_empresariales", []),
        "limites_declarados": data.get("riesgos_y_limites", []),
    }

    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(generar_informe_md(res), encoding="utf-8")
    output_json.write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
    return res


def crear_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Generador de informe Microsoft IA empresarial simulado.")
    p.add_argument("--results", required=True, type=Path)
    p.add_argument("--config", required=True, type=Path)
    p.add_argument("--output-md", required=True, type=Path)
    p.add_argument("--output-json", required=True, type=Path)
    return p


def main() -> None:
    a = crear_parser().parse_args()
    ejecutar(a.results, a.config, a.output_md, a.output_json)


if __name__ == "__main__":
    main()
