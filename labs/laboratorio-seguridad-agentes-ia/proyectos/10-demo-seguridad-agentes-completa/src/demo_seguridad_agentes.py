from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any


def cargar_json(r: Path) -> Any:
    with r.open("r", encoding="utf-8") as f:
        return json.load(f)


def construir_demo(esc: dict[str, Any], cfg: dict[str, Any]) -> dict[str, Any]:
    return {
        "fecha_generacion": datetime.now().isoformat(timespec="seconds"),
        "laboratorio": cfg["nombre_laboratorio"],
        "modo": cfg["modo"],
        "cadena_defensiva": [
            "inventario de riesgos",
            "simulación defensiva",
            "detección de entradas",
            "clasificación de sensibilidad",
            "control de herramientas",
            "políticas de uso",
            "trazabilidad de incidentes",
            "matriz de riesgo",
            "informe defensivo",
            "demo final"
        ],
        "riesgos_identificados": esc["riesgos_simulados"],
        "controles_aplicados": esc["controles_defensivos"],
        "incidentes_simulados": esc["incidentes_simulados"],
        "politicas_activadas": esc["politicas_internas_ficticias"],
        "decisiones_defensivas": ["bloquear", "revisar", "permitir_controlado"],
        "evidencias_generadas": ["EVI-TI-001", "EVI-TI-002", "EVI-TI-003"],
        "recomendaciones": ["Ampliar trazabilidad", "Reducir superficie de riesgo", "Mantener revisión humana"],
        "limites": cfg["limites"],
        "modulos_referenciados": cfg["modulos_representados"],
        "usa_datos_reales": cfg["usa_datos_reales"],
        "usa_ia_real": cfg["usa_ia_real"],
        "usa_api_externa": cfg["usa_api_externa"],
        "usa_cloud": cfg["usa_cloud"],
        "usa_herramienta_real": cfg["usa_herramienta_real"]
    }


def generar_markdowns(d: dict[str, Any], esc: dict[str, Any], out_dir: Path) -> None:
    guion = [
        "# Guion de Demo de Seguridad Defensiva para Agentes",
        "",
        "## Resumen ejecutivo",
        esc["conclusion_ejecutiva"],
        "",
        "## Narrativa de evaluación defensiva",
        "Cadena completa: inventario -> simulación -> detección -> sensibilidad -> herramientas -> políticas -> trazabilidad -> matriz -> informe -> demo.",
        "",
        "## Riesgos identificados",
    ] + [f"- {x}" for x in d["riesgos_identificados"]] + [
        "",
        "## Controles aplicados",
    ] + [f"- {x}" for x in d["controles_aplicados"]] + [
        "",
        "## Incidentes simulados",
    ] + [f"- {x}" for x in d["incidentes_simulados"]] + [
        "",
        "## Recomendaciones",
    ] + [f"- {x}" for x in d["recomendaciones"]] + [
        "",
        "## 🪪 Licencia y Autoría",
        "Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  ",
        "© 2025 – Txema Ríos. Todos los derechos compartidos.",
    ]
    (out_dir / "guion_demo_seguridad_agentes.md").write_text("\n".join(guion) + "\n", encoding="utf-8")

    expediente = [
        "# Expediente de Seguridad Defensiva de Agentes",
        "",
        f"Fecha: {d['fecha_generacion']}",
        "",
        "## Decisiones defensivas",
    ] + [f"- {x}" for x in d["decisiones_defensivas"]] + [
        "",
        "## Evidencias generadas",
    ] + [f"- {x}" for x in d["evidencias_generadas"]] + [
        "",
        "## Relación con los 10 módulos",
    ] + [f"- {x}" for x in d["modulos_referenciados"]] + [
        "",
        "## Límites",
    ] + [f"- {x}" for x in d["limites"]] + [
        "",
        "## 🪪 Licencia y Autoría",
        "Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  ",
        "© 2025 – Txema Ríos. Todos los derechos compartidos.",
    ]
    (out_dir / "expediente_seguridad_agentes.md").write_text("\n".join(expediente) + "\n", encoding="utf-8")

    mapa = [
        "# Mapa de Controles Defensivos",
        "",
        "## Controles",
    ] + [f"- {x}" for x in d["controles_aplicados"]] + [
        "",
        "## Políticas activadas",
    ] + [f"- {x}" for x in d["politicas_activadas"]] + [
        "",
        "## 🪪 Licencia y Autoría",
        "Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  ",
        "© 2025 – Txema Ríos. Todos los derechos compartidos.",
    ]
    (out_dir / "mapa_controles_defensivos.md").write_text("\n".join(mapa) + "\n", encoding="utf-8")


def ejecutar(scenario: Path, config: Path, output_dir: Path) -> dict[str, Any]:
    esc = cargar_json(scenario)
    cfg = cargar_json(config)
    output_dir.mkdir(parents=True, exist_ok=True)
    d = construir_demo(esc, cfg)
    generar_markdowns(d, esc, output_dir)
    (output_dir / "demo_seguridad_agentes.json").write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    return d


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--scenario", required=True, type=Path)
    p.add_argument("--config", required=True, type=Path)
    p.add_argument("--output-dir", required=True, type=Path)
    a = p.parse_args()
    d = ejecutar(a.scenario, a.config, a.output_dir)
    print(f"Demo generada. Módulos referenciados: {len(d['modulos_referenciados'])}")


if __name__ == "__main__":
    main()
