import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

CAMPOS_OBLIGATORIOS = [
    "id_componente",
    "nombre_componente",
    "categoria",
    "capa_arquitectura",
    "descripcion",
    "uso_empresarial_simulado",
    "entrada_sintetica",
    "salida_sintetica",
    "dependencia_real_obligatoria",
    "requiere_oauth_real",
    "requiere_api_real",
    "requiere_azure",
    "v1_local_simulada",
    "v2_opcional",
    "riesgos_y_limites",
    "nota_sintetica",
]


def cargar_json(ruta: Path) -> dict:
    with ruta.open("r", encoding="utf-8") as archivo:
        return json.load(archivo)


def validar_componentes(componentes: list[dict], config: dict) -> None:
    categorias = set(config.get("categorias_permitidas", []))
    capas = set(config.get("capas_arquitectura", []))

    for i, comp in enumerate(componentes, start=1):
        faltantes = [campo for campo in CAMPOS_OBLIGATORIOS if campo not in comp]
        if faltantes:
            raise ValueError(f"Componente {i} invalido. Faltan campos: {faltantes}")
        if comp["categoria"] not in categorias:
            raise ValueError(f"Categoria no permitida en {comp['id_componente']}: {comp['categoria']}")
        if comp["capa_arquitectura"] not in capas:
            raise ValueError(f"Capa no permitida en {comp['id_componente']}: {comp['capa_arquitectura']}")

        for bandera in [
            "dependencia_real_obligatoria",
            "requiere_oauth_real",
            "requiere_api_real",
            "requiere_azure",
        ]:
            if comp[bandera] is not False:
                raise ValueError(f"{comp['id_componente']} incumple politica local-first en {bandera}")

        if comp["v1_local_simulada"] is not True:
            raise ValueError(f"{comp['id_componente']} debe declarar v1_local_simulada=true")


def agrupar_por_clave(componentes: list[dict], clave: str) -> dict[str, list[dict]]:
    grupos = defaultdict(list)
    for comp in componentes:
        grupos[comp[clave]].append(comp)
    return dict(grupos)


def componentes_v2_opcional(componentes: list[dict]) -> list[dict]:
    candidatos = []
    for comp in componentes:
        texto = str(comp.get("v2_opcional", "")).lower()
        if "opcional" in texto or "graph" in texto or "copilot" in texto or "azure" in texto:
            candidatos.append(comp)
    return candidatos


def generar_mapa_textual(por_capa: dict[str, list[dict]]) -> str:
    lineas = []
    for capa in sorted(por_capa):
        nombres = ", ".join(sorted(c["nombre_componente"] for c in por_capa[capa]))
        lineas.append(f"- {capa}: {nombres}")
    return "\n".join(lineas)


def generar_informe_md(
    componentes: list[dict],
    por_categoria: dict[str, list[dict]],
    por_capa: dict[str, list[dict]],
    candidatos_v2: list[dict],
    config: dict,
) -> str:
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total = len(componentes)
    rel_m365 = [
        c["nombre_componente"]
        for c in componentes
        if any(
            x in c["nombre_componente"].lower()
            for x in ["outlook", "onedrive", "word", "excel", "teams", "planner", "to do"]
        )
    ]
    rel_copilot = [c["nombre_componente"] for c in componentes if "copilot" in c["nombre_componente"].lower()]
    rel_graph = [c["nombre_componente"] for c in componentes if "graph" in c["nombre_componente"].lower()]

    md = []
    md.append("# Informe de Mapa del Ecosistema Microsoft IA (Simulado)")
    md.append("")
    md.append(f"Fecha de generacion: {fecha}")
    md.append("")
    md.append("## Resumen ejecutivo")
    md.append(f"Se mapearon {total} componentes sinteticos del ecosistema Microsoft IA empresarial en modo local-first y free-first.")
    md.append("")
    md.append("## Componentes mapeados")
    for c in componentes:
        md.append(f"- {c['id_componente']}: {c['nombre_componente']} ({c['categoria']} / {c['capa_arquitectura']})")
    md.append("")
    md.append("## Mapa por capas")
    md.append(generar_mapa_textual(por_capa))
    md.append("")
    md.append("## Componentes por categoria")
    for categoria in sorted(por_categoria):
        md.append(f"- {categoria}: {len(por_categoria[categoria])}")
    md.append("")
    md.append("## Relacion con Microsoft 365")
    md.append("- " + ", ".join(rel_m365) if rel_m365 else "- No aplica en esta corrida.")
    md.append("")
    md.append("## Relacion con Copilot futuro opcional")
    md.append("- " + ", ".join(rel_copilot) if rel_copilot else "- No aplica en esta corrida.")
    md.append("")
    md.append("## Relacion con Microsoft Graph API futura opcional")
    md.append("- " + ", ".join(rel_graph) if rel_graph else "- No aplica en esta corrida.")
    md.append("")
    md.append("## Limites de la V1 local")
    for limite in config.get("limites_v1", []):
        md.append(f"- {limite}")
    md.append("")
    md.append("## Posibles extensiones V2")
    for c in candidatos_v2:
        md.append(f"- {c['nombre_componente']}: {c['v2_opcional']}")
    md.append("")
    md.append("## Recomendaciones siguientes")
    md.append("- Mantener fallback local como requisito transversal.")
    md.append("- Diseñar contratos de integracion opcionales por componente.")
    md.append("- Definir pruebas de regresion para las salidas JSON y Markdown.")
    md.append("")
    md.append("## 🪪 Licencia y Autoría")
    md.append("Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  ")
    md.append("© 2025 – Txema Ríos. Todos los derechos compartidos.")
    return "\n".join(md) + "\n"


def ejecutar(ecosystem_path: Path, config_path: Path, output_md: Path, output_json: Path) -> dict:
    ecosystem = cargar_json(ecosystem_path)
    config = cargar_json(config_path)
    componentes = ecosystem.get("componentes", [])
    if not componentes:
        raise ValueError("No hay componentes en el ecosistema.")

    validar_componentes(componentes, config)
    por_categoria = agrupar_por_clave(componentes, "categoria")
    por_capa = agrupar_por_clave(componentes, "capa_arquitectura")
    candidatos_v2 = componentes_v2_opcional(componentes)

    salida = {
        "metadata": {
            "fecha_generacion": datetime.now().isoformat(timespec="seconds"),
            "total_componentes": len(componentes),
            "nota": config.get("nota", ""),
        },
        "resumen_por_categoria": dict(Counter(c["categoria"] for c in componentes)),
        "resumen_por_capa": dict(Counter(c["capa_arquitectura"] for c in componentes)),
        "candidatos_v2_opcional": [
            {
                "id_componente": c["id_componente"],
                "nombre_componente": c["nombre_componente"],
                "v2_opcional": c["v2_opcional"],
            }
            for c in candidatos_v2
        ],
        "componentes": componentes,
        "controles_v1": {
            "dependencia_real_obligatoria": False,
            "requiere_oauth_real": False,
            "requiere_api_real": False,
            "requiere_azure": False,
            "usa_ia_real": False,
            "usa_datos_reales": False,
        },
    }

    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(generar_informe_md(componentes, por_categoria, por_capa, candidatos_v2, config), encoding="utf-8")
    output_json.write_text(json.dumps(salida, ensure_ascii=False, indent=2), encoding="utf-8")
    return salida


def crear_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generador local de mapa del ecosistema Microsoft IA (simulado).")
    parser.add_argument("--ecosystem", required=True, type=Path)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--output-md", required=True, type=Path)
    parser.add_argument("--output-json", required=True, type=Path)
    return parser


def main() -> None:
    args = crear_parser().parse_args()
    ejecutar(args.ecosystem, args.config, args.output_md, args.output_json)


if __name__ == "__main__":
    main()
