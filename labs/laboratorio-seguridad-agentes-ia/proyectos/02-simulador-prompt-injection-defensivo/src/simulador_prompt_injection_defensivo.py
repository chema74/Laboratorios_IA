from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

SEVERIDAD_MAPA = {"baja": 1, "media": 2, "alta": 3, "critica": 4}
PLACEHOLDERS_PERMITIDOS = {
    "[INSTRUCCION_NO_ACCIONABLE]",
    "[SECRETO_FICTICIO]",
    "[HERRAMIENTA_SIMULADA]",
    "[POLITICA_INTERNA_FICTICIA]",
    "[DATOS_SINTETICOS]",
}


def cargar_json(ruta: Path) -> Any:
    with ruta.open("r", encoding="utf-8") as f:
        return json.load(f)


def validar_estructura_entrada(entrada: dict[str, Any]) -> list[str]:
    campos = [
        "id_entrada",
        "categoria_simulada",
        "texto_sintetico_no_accionable",
        "objetivo_simulado",
        "riesgo_defensivo_asociado",
        "politica_que_deberia_activarse",
        "severidad_simulada",
        "respuesta_segura_esperada",
        "controles_recomendados",
        "requiere_revision_humana",
        "limites_declarados",
        "usa_datos_reales",
        "usa_ia_real",
        "usa_api_externa",
        "usa_cloud",
        "nota_sintetica",
    ]
    return [f"Falta campo obligatorio: {c}" for c in campos if c not in entrada]


def validar_placeholders(texto: str) -> bool:
    return any(ph in texto for ph in PLACEHOLDERS_PERMITIDOS)


def puntuacion_riesgo_simulada(entrada: dict[str, Any]) -> float:
    base = float(SEVERIDAD_MAPA.get(entrada["severidad_simulada"], 1))
    if entrada.get("requiere_revision_humana"):
        base += 0.8
    if "[INSTRUCCION_NO_ACCIONABLE]" in entrada.get("texto_sintetico_no_accionable", ""):
        base += 0.4
    return round(base, 2)


def clasificar_entrada(entrada: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    categoria = entrada["categoria_simulada"]
    politica = entrada["politica_que_deberia_activarse"]
    salida = dict(entrada)
    salida["clasificacion_defensiva"] = config["reglas_clasificacion_defensiva"].get(categoria, "riesgo no clasificado")
    salida["politica_activada_descripcion"] = config["politicas_defensivas"].get(politica, "Política no definida.")
    salida["puntuacion_riesgo_simulada"] = puntuacion_riesgo_simulada(entrada)
    return salida


def simular(entradas: list[dict[str, Any]], config: dict[str, Any]) -> dict[str, Any]:
    errores: list[str] = []
    resultados: list[dict[str, Any]] = []
    for entrada in entradas:
        err = validar_estructura_entrada(entrada)
        if entrada.get("categoria_simulada") not in config["categorias_permitidas"]:
            err.append(f"Categoría no permitida: {entrada.get('categoria_simulada')}")
        if entrada.get("severidad_simulada") not in config["severidades_permitidas"]:
            err.append(f"Severidad no permitida: {entrada.get('severidad_simulada')}")
        if not validar_placeholders(entrada.get("texto_sintetico_no_accionable", "")):
            err.append("El texto no incluye placeholders ficticios obligatorios")
        for bandera in ("usa_datos_reales", "usa_ia_real", "usa_api_externa", "usa_cloud"):
            if entrada.get(bandera) is not False:
                err.append(f"{bandera} debe ser false")
        if err:
            errores.append(f"{entrada.get('id_entrada', 'SIN_ID')}: " + " | ".join(err))
            continue
        resultados.append(clasificar_entrada(entrada, config))

    return {
        "fecha_generacion": datetime.now().isoformat(timespec="seconds"),
        "total_entradas_simuladas": len(resultados),
        "errores_validacion": errores,
        "distribucion_por_categoria": dict(Counter(r["categoria_simulada"] for r in resultados)),
        "distribucion_por_severidad": dict(Counter(r["severidad_simulada"] for r in resultados)),
        "politicas_activadas": dict(Counter(r["politica_que_deberia_activarse"] for r in resultados)),
        "entradas_revision_humana": [r for r in resultados if r.get("requiere_revision_humana")],
        "controles_recomendados_globales": config["controles_recomendados"],
        "resultados": resultados,
    }


def generar_markdown(resultado: dict[str, Any]) -> str:
    lineas = [
        "# Informe de Simulación Defensiva de Prompt Injection (Sintética)",
        "",
        f"Fecha de generación: {resultado['fecha_generacion']}",
        "",
        "## Resumen ejecutivo",
        "Simulación local y segura de entradas sintéticas no accionables para evaluar políticas defensivas y trazabilidad.",
        "",
        "## Total de entradas simuladas",
        str(resultado["total_entradas_simuladas"]),
        "",
        "## Distribución por categoría",
    ]
    lineas.extend([f"- {k}: {v}" for k, v in resultado["distribucion_por_categoria"].items()])
    lineas += ["", "## Distribución por severidad"]
    lineas.extend([f"- {k}: {v}" for k, v in resultado["distribucion_por_severidad"].items()])
    lineas += ["", "## Políticas defensivas activadas"]
    lineas.extend([f"- {k}: {v}" for k, v in resultado["politicas_activadas"].items()])
    lineas += ["", "## Entradas que requieren revisión humana"]
    if resultado["entradas_revision_humana"]:
        lineas.extend([f"- {r['id_entrada']} - {r['categoria_simulada']}" for r in resultado["entradas_revision_humana"]])
    else:
        lineas.append("- No se detectaron entradas que requieran revisión humana.")
    lineas += ["", "## Ejemplos seguros y no accionables"]
    lineas.extend([f"- {r['id_entrada']}: {r['texto_sintetico_no_accionable']}" for r in resultado["resultados"][:3]])
    lineas += [
        "",
        "## Lectura técnica defensiva",
        "Los resultados permiten verificar activación de políticas, priorizar revisión humana y reforzar controles.",
        "",
        "## Límites de la simulación",
        "No incluye ataques reales, explotación, IA real, APIs externas, cloud ni datos reales.",
        "",
        "## Recomendaciones siguientes",
        "1. Ampliar cobertura de categorías simuladas.",
        "2. Revisar políticas con mayor frecuencia en severidad crítica.",
        "3. Mejorar trazabilidad de decisiones para auditoría defensiva.",
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
        raise ValueError("El archivo de entradas debe contener una lista JSON")
    if not isinstance(config, dict):
        raise ValueError("El archivo de configuración debe contener un objeto JSON")
    resultado = simular(entradas, config)
    salida_md.parent.mkdir(parents=True, exist_ok=True)
    salida_json.parent.mkdir(parents=True, exist_ok=True)
    salida_md.write_text(generar_markdown(resultado), encoding="utf-8")
    salida_json.write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8")
    return resultado


def main() -> None:
    parser = argparse.ArgumentParser(description="Simulador local defensivo de prompt injection sintética.")
    parser.add_argument("--inputs", required=True, type=Path)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--output-md", required=True, type=Path)
    parser.add_argument("--output-json", required=True, type=Path)
    args = parser.parse_args()
    resultado = ejecutar(args.inputs, args.config, args.output_md, args.output_json)
    print(f"Simulación generada. Entradas válidas: {resultado['total_entradas_simuladas']}")


if __name__ == "__main__":
    main()
