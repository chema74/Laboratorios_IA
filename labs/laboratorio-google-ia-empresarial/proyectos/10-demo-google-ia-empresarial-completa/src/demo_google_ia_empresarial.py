"""Demo local completa del laboratorio Google IA empresarial simulado."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path


def cargar_json(ruta: Path) -> dict:
    with ruta.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def construir_demo(escenario: dict, config: dict) -> dict:
    return {
        "metadatos": {"fecha_generacion": datetime.now().isoformat(timespec="seconds"), "modo": config["modo"]},
        "empresa_ficticia": escenario["empresa_ficticia"],
        "resumen_ejecutivo": "Demo integradora local de los 10 módulos del laboratorio Google IA empresarial.",
        "narrativa_empresarial": escenario["contexto_operativo_sintetico"],
        "recorrido_modulos": config["modulos_representados"],
        "cadena_completa": [
            "mapa del ecosistema",
            "gmail simulado",
            "drive/docs simulados",
            "sheets analítico",
            "calendar/tareas",
            "gemini fallback local",
            "gobierno de permisos",
            "trazabilidad",
            "informe empresarial",
            "demo final",
        ],
        "evidencias_simuladas": ["json_locales", "markdown_locales", "registros_locales"],
        "automatizaciones_simuladas": escenario["automatizaciones_simuladas"],
        "permisos_y_gobierno": escenario["permisos_simulados"],
        "trazabilidad": "hash_y_traza_local",
        "recomendaciones": ["mantener_fallback", "mejorar_controles", "documentar_v2_opcional"],
        "limites": config["limites"],
        "relacion_v2_futura": "Integración opcional por .env manteniendo fallback local.",
        "usa_google_real": config["usa_google_real"],
        "usa_oauth_real": config["usa_oauth_real"],
        "usa_api_externa": config["usa_api_externa"],
        "usa_cloud": config["usa_cloud"],
        "usa_ia_real": config["usa_ia_real"],
        "usa_datos_reales": config["usa_datos_reales"],
    }


def escribir_archivos(demo: dict, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "demo_google_ia_empresarial.json").write_text(json.dumps(demo, ensure_ascii=False, indent=2), encoding="utf-8")

    guion = [
        "# Guion Demo Google IA Empresarial",
        "",
        "## Resumen ejecutivo",
        demo["resumen_ejecutivo"],
        "",
        "## Recorrido por módulos",
    ]
    for m in demo["recorrido_modulos"]:
        guion.append(f"- Módulo {m}")
    guion.extend(
        [
            "",
            "## Límites",
            "- Sin Google real, sin OAuth real, sin APIs reales, sin cloud real, sin IA real.",
            "",
            "## 🪪 Licencia y Autoría",
            "Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  ",
            "© 2025 – Txema Ríos. Todos los derechos compartidos.",
        ]
    )
    (output_dir / "guion_demo_google_ia_empresarial.md").write_text("\n".join(guion), encoding="utf-8")

    expediente = [
        "# Expediente Google IA Empresarial",
        "",
        "## Narrativa empresarial de uso",
        demo["narrativa_empresarial"],
        "",
        "## Evidencias simuladas",
    ]
    for e in demo["evidencias_simuladas"]:
        expediente.append(f"- {e}")
    expediente.extend(
        [
            "",
            "## Recomendaciones",
        ]
    )
    for r in demo["recomendaciones"]:
        expediente.append(f"- {r}")
    expediente.extend(
        [
            "",
            "## 🪪 Licencia y Autoría",
            "Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  ",
            "© 2025 – Txema Ríos. Todos los derechos compartidos.",
        ]
    )
    (output_dir / "expediente_google_ia_empresarial.md").write_text("\n".join(expediente), encoding="utf-8")

    mapa = [
        "# Mapa de Componentes Google IA",
        "",
        "mapa del ecosistema -> Gmail simulado -> Drive/Docs simulados -> Sheets -> Calendar -> Gemini fallback -> Gobierno -> Trazabilidad -> Informe -> Demo",
        "",
        "## 🪪 Licencia y Autoría",
        "Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  ",
        "© 2025 – Txema Ríos. Todos los derechos compartidos.",
    ]
    (output_dir / "mapa_componentes_google_ia.md").write_text("\n".join(mapa), encoding="utf-8")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--scenario", required=True)
    p.add_argument("--config", required=True)
    p.add_argument("--output-dir", required=True)
    a = p.parse_args()
    escenario = cargar_json(Path(a.scenario))
    config = cargar_json(Path(a.config))
    demo = construir_demo(escenario, config)
    escribir_archivos(demo, Path(a.output_dir))


if __name__ == "__main__":
    main()
