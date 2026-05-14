"""Generador local de mapa del ecosistema Google IA empresarial (simulado)."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

CAMPOS_COMPONENTE = {
    "id_componente",
    "nombre_componente",
    "categoria",
    "descripcion",
    "uso_empresarial_simulado",
    "entrada_sintetica",
    "salida_sintetica",
    "dependencia_real_obligatoria",
    "requiere_oauth_real",
    "requiere_api_real",
    "requiere_cloud",
    "v1_local_simulada",
    "v2_opcional",
    "riesgos_y_limites",
    "nota_sintetica",
    "capa_arquitectura",
}


def cargar_json(ruta: Path) -> dict:
    with ruta.open("r", encoding="utf-8-sig") as archivo:
        return json.load(archivo)


def validar_componentes(componentes: list[dict], config: dict) -> None:
    categorias = set(config.get("categorias_permitidas", []))
    capas = set(config.get("capas_arquitectura", []))
    if not componentes:
        raise ValueError("No hay componentes en el ecosistema.")

    for indice, componente in enumerate(componentes, start=1):
        faltantes = CAMPOS_COMPONENTE.difference(componente.keys())
        if faltantes:
            raise ValueError(f"Componente {indice} incompleto: faltan {sorted(faltantes)}")
        if componente["categoria"] not in categorias:
            raise ValueError(f"Categoría no permitida: {componente['categoria']}")
        if componente["capa_arquitectura"] not in capas:
            raise ValueError(f"Capa no permitida: {componente['capa_arquitectura']}")


def clasificar_por_clave(componentes: list[dict], clave: str) -> dict[str, list[dict]]:
    agrupado: dict[str, list[dict]] = defaultdict(list)
    for componente in componentes:
        agrupado[componente[clave]].append(componente)
    return dict(agrupado)


def detectar_v2_opcional(componentes: list[dict]) -> list[dict]:
    candidatos = []
    for componente in componentes:
        texto_v2 = str(componente.get("v2_opcional", "")).lower()
        if any(token in texto_v2 for token in ("api", "workspace", "cloud", ".env", "oauth")):
            candidatos.append(
                {
                    "id_componente": componente["id_componente"],
                    "nombre_componente": componente["nombre_componente"],
                    "v2_opcional": componente["v2_opcional"],
                }
            )
    return candidatos


def verificar_dependencias_reales(componentes: list[dict]) -> None:
    for componente in componentes:
        if componente["dependencia_real_obligatoria"]:
            raise ValueError(f"Dependencia real obligatoria detectada en {componente['id_componente']}")


def construir_mapa_textual(por_capa: dict[str, list[dict]]) -> str:
    lineas = []
    for capa, elementos in por_capa.items():
        nombres = ", ".join(item["nombre_componente"] for item in elementos)
        lineas.append(f"- {capa}: {nombres}")
    return "\n".join(lineas)


def generar_informe_markdown(resultado: dict, salida: Path) -> None:
    lineas = [
        "# Informe de Mapa del Ecosistema Google IA (Simulado)",
        "",
        f"**Fecha de generación:** {resultado['fecha_generacion']}",
        "",
        "## Resumen ejecutivo",
        f"Se mapearon {resultado['total_componentes']} componentes sintéticos con enfoque local-first y free-first.",
        "",
        "## Componentes mapeados",
    ]
    for comp in resultado["componentes"]:
        lineas.append(f"- {comp['id_componente']} | {comp['nombre_componente']} | {comp['categoria']} | {comp['capa_arquitectura']}")

    lineas.extend(["", "## Mapa por capas"])
    for capa, cantidad in resultado["resumen_por_capa"].items():
        lineas.append(f"- {capa}: {cantidad}")

    lineas.extend(["", "## Componentes por categoría"])
    for categoria, cantidad in resultado["resumen_por_categoria"].items():
        lineas.append(f"- {categoria}: {cantidad}")

    lineas.extend(
        [
            "",
            "## Relación con Google Workspace",
            "La V1 usa representaciones simuladas de Gmail, Drive, Docs, Sheets y Calendar sin conexión a servicios reales.",
            "",
            "## Relación con Gemini futura opcional",
            "Gemini solo aparece como extensión opcional V2 mediante `.env`, con fallback local obligatorio.",
            "",
            "## Límites de la V1 local",
            "Sin OAuth real, sin APIs reales, sin Google Cloud obligatorio, sin datos reales y sin IA real ejecutándose.",
            "",
            "## Posibles extensiones V2",
        ]
    )
    for candidato in resultado["componentes_v2_opcional"]:
        lineas.append(f"- {candidato['nombre_componente']}: {candidato['v2_opcional']}")

    lineas.extend(
        [
            "",
            "## Recomendaciones siguientes",
            "1. Definir contratos de integración opcional por componente con fallback local.",
            "2. Añadir validaciones adicionales de trazabilidad cruzada entre módulos.",
            "3. Incorporar métricas de madurez por capa arquitectónica.",
            "",
            "## 🪪 Licencia y Autoría",
            "Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  ",
            "© 2025 – Txema Ríos. Todos los derechos compartidos.",
        ]
    )
    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.write_text("\n".join(lineas), encoding="utf-8")


def generar_resultado(ecosystem_data: dict, config_data: dict) -> dict:
    componentes = ecosystem_data["componentes"]
    validar_componentes(componentes, config_data)
    verificar_dependencias_reales(componentes)
    por_categoria = clasificar_por_clave(componentes, "categoria")
    por_capa = clasificar_por_clave(componentes, "capa_arquitectura")
    return {
        "fecha_generacion": datetime.now().isoformat(timespec="seconds"),
        "total_componentes": len(componentes),
        "componentes": componentes,
        "resumen_por_categoria": dict(Counter(comp["categoria"] for comp in componentes)),
        "resumen_por_capa": dict(Counter(comp["capa_arquitectura"] for comp in componentes)),
        "componentes_por_categoria": {k: [x["id_componente"] for x in v] for k, v in por_categoria.items()},
        "componentes_por_capa": {k: [x["id_componente"] for x in v] for k, v in por_capa.items()},
        "componentes_v2_opcional": detectar_v2_opcional(componentes),
        "mapa_conceptual_textual": construir_mapa_textual(por_capa),
        "limites_v1": config_data.get("limites_v1", []),
        "nota": config_data.get("nota", ""),
    }


def parsear_argumentos() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Genera mapa de ecosistema Google IA simulado.")
    parser.add_argument("--ecosystem", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output-md", required=True)
    parser.add_argument("--output-json", required=True)
    return parser.parse_args()


def main() -> None:
    args = parsear_argumentos()
    ecosystem_data = cargar_json(Path(args.ecosystem))
    config_data = cargar_json(Path(args.config))
    resultado = generar_resultado(ecosystem_data, config_data)
    out_json = Path(args.output_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8")
    generar_informe_markdown(resultado, Path(args.output_md))


if __name__ == "__main__":
    main()
