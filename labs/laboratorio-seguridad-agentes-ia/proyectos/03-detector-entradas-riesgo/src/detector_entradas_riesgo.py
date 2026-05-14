from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any


def cargar_json(ruta: Path) -> Any:
    with ruta.open("r", encoding="utf-8") as f:
        return json.load(f)


def validar_estructura_entrada(entrada: dict[str, Any]) -> list[str]:
    campos = [
        "id_entrada",
        "canal_simulado",
        "texto_sintetico_no_accionable",
        "categoria_riesgo_esperada",
        "severidad_esperada",
        "politica_defensiva_esperada",
        "requiere_bloqueo",
        "requiere_revision_humana",
        "explicacion_defensiva",
        "limites_declarados",
        "usa_datos_reales",
        "usa_ia_real",
        "usa_api_externa",
        "usa_cloud",
        "nota_sintetica",
    ]
    return [f"Falta campo obligatorio: {c}" for c in campos if c not in entrada]


def contiene_placeholder(texto: str) -> bool:
    return bool(re.search(r"\[[A-Z_]+\]", texto))


def detectar_categoria(texto: str, config: dict[str, Any]) -> str:
    texto_lower = texto.lower()
    for categoria, patrones in config["patrones_defensivos_simulados"].items():
        for patron in patrones:
            if patron.lower() in texto_lower:
                return categoria
    return "petición ambigua de alto riesgo"


def severidad_por_categoria(categoria: str) -> str:
    mapa = {
        "intento simulado de revelar secreto ficticio": "critica",
        "solicitud fuera de política simulada": "alta",
        "uso no permitido de herramienta simulada": "alta",
        "solicitud con datos sintéticos sensibles": "media",
    }
    return mapa.get(categoria, "media")


def analizar_entrada(entrada: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    categoria = detectar_categoria(entrada["texto_sintetico_no_accionable"], config)
    severidad = severidad_por_categoria(categoria)
    politica = config["politicas_defensivas"].get(categoria, "escalado_revision_humana")
    bloqueo = categoria in config["reglas_bloqueo"]
    revision = categoria in config["reglas_revision_humana"] or entrada.get("requiere_revision_humana", False)
    control = config["controles_recomendados"][0] if bloqueo else config["controles_recomendados"][2]

    salida = dict(entrada)
    salida["categoria_detectada"] = categoria
    salida["severidad_simulada"] = severidad
    salida["politica_activada"] = politica
    salida["marcar_bloqueo"] = bloqueo
    salida["marcar_revision_humana"] = revision
    salida["recomendacion_control"] = control
    salida["explicacion_detector"] = (
        f"Se detecta categoría '{categoria}' por patrones defensivos sintéticos y se activa '{politica}'."
    )
    return salida


def ejecutar_analisis(entradas: list[dict[str, Any]], config: dict[str, Any]) -> dict[str, Any]:
    errores: list[str] = []
    resultados: list[dict[str, Any]] = []
    for entrada in entradas:
        err = validar_estructura_entrada(entrada)
        if entrada.get("categoria_riesgo_esperada") not in config["categorias_permitidas"]:
            err.append("categoria_riesgo_esperada fuera de catálogo")
        if entrada.get("severidad_esperada") not in config["severidades_permitidas"]:
            err.append("severidad_esperada no permitida")
        if not contiene_placeholder(entrada.get("texto_sintetico_no_accionable", "")):
            err.append("texto sin placeholders ficticios")
        for bandera in ("usa_datos_reales", "usa_ia_real", "usa_api_externa", "usa_cloud"):
            if entrada.get(bandera) is not False:
                err.append(f"{bandera} debe ser false")
        if err:
            errores.append(f"{entrada.get('id_entrada', 'SIN_ID')}: " + " | ".join(err))
            continue
        resultados.append(analizar_entrada(entrada, config))

    return {
        "fecha_generacion": datetime.now().isoformat(timespec="seconds"),
        "total_entradas_analizadas": len(resultados),
        "errores_validacion": errores,
        "distribucion_por_categoria": dict(Counter(r["categoria_detectada"] for r in resultados)),
        "distribucion_por_severidad": dict(Counter(r["severidad_simulada"] for r in resultados)),
        "entradas_bloqueables": [r for r in resultados if r["marcar_bloqueo"]],
        "entradas_revision_humana": [r for r in resultados if r["marcar_revision_humana"]],
        "politicas_activadas": dict(Counter(r["politica_activada"] for r in resultados)),
        "controles_recomendados": config["controles_recomendados"],
        "resultados": resultados,
    }


def generar_markdown(resultado: dict[str, Any]) -> str:
    lineas = [
        "# Informe del Detector Defensivo de Entradas de Riesgo",
        "",
        f"Fecha de generación: {resultado['fecha_generacion']}",
        "",
        "## Resumen ejecutivo",
        "Análisis local de entradas sintéticas no accionables para detectar riesgo, activar políticas y reforzar trazabilidad.",
        "",
        "## Total de entradas analizadas",
        str(resultado["total_entradas_analizadas"]),
        "",
        "## Distribución por categoría",
    ]
    lineas.extend([f"- {k}: {v}" for k, v in resultado["distribucion_por_categoria"].items()])
    lineas += ["", "## Distribución por severidad"]
    lineas.extend([f"- {k}: {v}" for k, v in resultado["distribucion_por_severidad"].items()])
    lineas += ["", "## Entradas bloqueables"]
    lineas.extend([f"- {r['id_entrada']} - {r['categoria_detectada']}" for r in resultado["entradas_bloqueables"]] or ["- Ninguna"])
    lineas += ["", "## Entradas que requieren revisión humana"]
    lineas.extend([f"- {r['id_entrada']} - {r['categoria_detectada']}" for r in resultado["entradas_revision_humana"]] or ["- Ninguna"])
    lineas += ["", "## Políticas defensivas activadas"]
    lineas.extend([f"- {k}: {v}" for k, v in resultado["politicas_activadas"].items()])
    lineas += ["", "## Controles recomendados"]
    lineas.extend([f"- {c}" for c in resultado["controles_recomendados"]])
    lineas += [
        "",
        "## Lectura técnica defensiva",
        "Las entradas con marcadores sensibles o conflicto de política se priorizan para bloqueo y revisión humana.",
        "",
        "## Límites del detector",
        "Clasificación basada en reglas simples y placeholders sintéticos, no aplicable a producción.",
        "",
        "## Recomendaciones siguientes",
        "1. Ampliar patrones defensivos simulados por canal.",
        "2. Reforzar cobertura de políticas de revisión humana.",
        "3. Integrar resultados con matriz de riesgo del proyecto 08.",
        "",
        "## 🪪 Licencia y Autoría",
        "Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  ",
        "© 2025 – Txema Ríos. Todos los derechos compartidos.",
    ]
    return "\n".join(lineas) + "\n"


def ejecutar(ruta_inputs: Path, ruta_config: Path, salida_md: Path, salida_json: Path) -> dict[str, Any]:
    entradas = cargar_json(ruta_inputs)
    config = cargar_json(ruta_config)
    if not isinstance(entradas, list):
        raise ValueError("inputs debe ser lista")
    if not isinstance(config, dict):
        raise ValueError("config debe ser objeto")
    resultado = ejecutar_analisis(entradas, config)
    salida_md.parent.mkdir(parents=True, exist_ok=True)
    salida_json.parent.mkdir(parents=True, exist_ok=True)
    salida_md.write_text(generar_markdown(resultado), encoding="utf-8")
    salida_json.write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8")
    return resultado


def main() -> None:
    parser = argparse.ArgumentParser(description="Detector local defensivo de entradas de riesgo sintéticas.")
    parser.add_argument("--inputs", required=True, type=Path)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--output-md", required=True, type=Path)
    parser.add_argument("--output-json", required=True, type=Path)
    args = parser.parse_args()
    resultado = ejecutar(args.inputs, args.config, args.output_md, args.output_json)
    print(f"Detección completada. Entradas válidas: {resultado['total_entradas_analizadas']}")


if __name__ == "__main__":
    main()
