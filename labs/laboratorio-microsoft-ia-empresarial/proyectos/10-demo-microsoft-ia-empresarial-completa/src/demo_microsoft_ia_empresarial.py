import argparse
import json
from datetime import datetime
from pathlib import Path


def cargar_json(ruta: Path) -> dict:
    with ruta.open("r", encoding="utf-8") as f:
        return json.load(f)


def validar_config(cfg: dict) -> None:
    if cfg["modo"] != "local-simulado":
        raise ValueError("La demo V1 debe ser local-simulado.")
    for b in [
        "usa_microsoft_real",
        "usa_microsoft_graph_real",
        "usa_oauth_real",
        "usa_api_externa",
        "usa_azure",
        "usa_ia_real",
        "usa_datos_reales",
    ]:
        if cfg[b] is not False:
            raise ValueError(f"Configuracion invalida en {b}")


def generar_guion_md(esc: dict, cfg: dict) -> str:
    modulos = cfg["modulos_representados"]
    lineas = [
        "# Guion Demo Microsoft IA Empresarial",
        "",
        "## Resumen ejecutivo",
        f"Demostración local de {cfg['nombre_laboratorio_ficticio']} en cadena completa de 10 módulos simulados.",
        "",
        "## Narrativa empresarial de uso",
        esc["contexto_operativo_sintetico"],
        "",
        "## Recorrido por módulos",
    ]
    for m in modulos:
        lineas.append(f"- {m}")
    lineas.extend(
        [
            "",
            "## Cadena completa",
            "mapa del ecosistema -> Outlook simulado -> OneDrive/Word simulados -> Excel analítico -> Teams/tareas -> Copilot fallback local -> gobierno de permisos -> trazabilidad -> informe empresarial -> demo final.",
            "",
            "## Evidencias simuladas",
            "- Informes markdown por módulo.",
            "- Salidas JSON reproducibles.",
            "- Registros locales de ejecución.",
            "",
            "## Límites",
        ]
    )
    for l in cfg["limites"]:
        lineas.append(f"- {l}")
    lineas.extend(
        [
            "",
            "## Relación con V2 futura opcional",
            "- Posible integración real vía .env, manteniendo fallback local obligatorio.",
            "",
            "## 🪪 Licencia y Autoría",
            "Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  ",
            "© 2025 – Txema Ríos. Todos los derechos compartidos.",
            "",
        ]
    )
    return "\n".join(lineas)


def generar_expediente_md(esc: dict, cfg: dict) -> str:
    l = [
        "# Expediente Microsoft IA Empresarial (Demo Local)",
        "",
        f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## Empresa ficticia",
        f"- {esc['empresa_ficticia']}",
        "",
        "## Componentes simulados",
        f"- Outlook: {esc['outlook_simulado']}",
        f"- OneDrive/Word: {esc['documentos_word_simulados']}",
        f"- Excel: {esc['libro_excel_operativo_simulado']}",
        f"- Teams/tareas: {esc['teams_reuniones_tareas_simuladas']}",
        f"- Copilot fallback: {esc['solicitudes_copilot_fallback']}",
        f"- Gobierno: {esc['permisos_simulados']}",
        f"- Trazabilidad: {esc['automatizaciones_simuladas']}",
        "",
        "## Riesgos y límites",
    ]
    for x in esc["riesgos_y_limites"]:
        l.append(f"- {x}")
    l.extend(
        [
            "",
            "## Conclusión ejecutiva",
            esc["conclusion_ejecutiva"],
            "",
            "## 🪪 Licencia y Autoría",
            "Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  ",
            "© 2025 – Txema Ríos. Todos los derechos compartidos.",
            "",
        ]
    )
    return "\n".join(l)


def generar_mapa_componentes_md(cfg: dict) -> str:
    l = [
        "# Mapa de Componentes Microsoft IA (Demo)",
        "",
        "## Componentes representados",
    ]
    for m in cfg["modulos_representados"]:
        l.append(f"- {m}")
    l.extend(
        [
            "",
            "## Flujo",
            "01 -> 02 -> 03 -> 04 -> 05 -> 06 -> 07 -> 08 -> 09 -> 10",
            "",
            "## 🪪 Licencia y Autoría",
            "Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  ",
            "© 2025 – Txema Ríos. Todos los derechos compartidos.",
            "",
        ]
    )
    return "\n".join(l)


def ejecutar(scenario_path: Path, config_path: Path, output_dir: Path) -> dict:
    esc = cargar_json(scenario_path)
    cfg = cargar_json(config_path)
    validar_config(cfg)

    output_dir.mkdir(parents=True, exist_ok=True)
    guion = output_dir / "guion_demo_microsoft_ia_empresarial.md"
    expediente = output_dir / "expediente_microsoft_ia_empresarial.md"
    mapa = output_dir / "mapa_componentes_microsoft_ia.md"
    salida_json = output_dir / "demo_microsoft_ia_empresarial.json"

    guion.write_text(generar_guion_md(esc, cfg), encoding="utf-8")
    expediente.write_text(generar_expediente_md(esc, cfg), encoding="utf-8")
    mapa.write_text(generar_mapa_componentes_md(cfg), encoding="utf-8")

    salida = {
        "metadatos": {
            "fecha_generacion": datetime.now().isoformat(timespec="seconds"),
            "modo": cfg["modo"],
            "nombre_laboratorio_ficticio": cfg["nombre_laboratorio_ficticio"],
        },
        "resumen_ejecutivo": "Demo local completa del laboratorio Microsoft IA empresarial simulado.",
        "narrativa_empresarial": esc["contexto_operativo_sintetico"],
        "modulos_representados": cfg["modulos_representados"],
        "evidencias_simuladas": {
            "guion": str(guion),
            "expediente": str(expediente),
            "mapa_componentes": str(mapa),
        },
        "automatizaciones_simuladas": esc["automatizaciones_simuladas"],
        "permisos_y_gobierno": esc["permisos_simulados"],
        "trazabilidad": "Incluida por integración conceptual del módulo 08.",
        "recomendaciones": cfg["criterios_demo"],
        "limites": cfg["limites"],
        "v2_futura_opcional": "Integración real opcional vía .env con fallback local obligatorio.",
        "usa_microsoft_real": False,
        "usa_microsoft_graph_real": False,
        "usa_oauth_real": False,
        "usa_api_externa": False,
        "usa_azure": False,
        "usa_ia_real": False,
        "usa_datos_reales": False,
    }
    salida_json.write_text(json.dumps(salida, ensure_ascii=False, indent=2), encoding="utf-8")
    return salida


def crear_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Demo local completa Microsoft IA empresarial.")
    p.add_argument("--scenario", required=True, type=Path)
    p.add_argument("--config", required=True, type=Path)
    p.add_argument("--output-dir", required=True, type=Path)
    return p


def main() -> None:
    a = crear_parser().parse_args()
    ejecutar(a.scenario, a.config, a.output_dir)


if __name__ == "__main__":
    main()
