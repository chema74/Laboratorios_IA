from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

SEVERIDAD_MAPA = {"baja": 1, "media": 2, "alta": 3, "critica": 4}


def cargar_json(ruta: Path) -> Any:
    with ruta.open("r", encoding="utf-8") as f:
        return json.load(f)


def validar_estructura_riesgo(riesgo: dict[str, Any]) -> list[str]:
    campos = [
        "id_riesgo",
        "nombre_riesgo",
        "categoria",
        "descripcion_defensiva",
        "vector_simulado",
        "impacto_operativo_simulado",
        "impacto_privacidad_simulado",
        "impacto_seguridad_simulado",
        "probabilidad_simulada",
        "severidad",
        "detectabilidad",
        "controles_defensivos",
        "evidencias_recomendadas",
        "responsable_simulado",
        "estado_control",
        "limites_declarados",
        "usa_datos_reales",
        "usa_ia_real",
        "usa_api_externa",
        "usa_cloud",
        "nota_sintetica",
    ]
    return [f"Falta campo obligatorio: {c}" for c in campos if c not in riesgo]


def validar_riesgo(riesgo: dict[str, Any], config: dict[str, Any]) -> list[str]:
    errores = validar_estructura_riesgo(riesgo)
    if riesgo.get("categoria") not in config["categorias_permitidas"]:
        errores.append(f"Categoría no permitida: {riesgo.get('categoria')}")
    if riesgo.get("severidad") not in config["severidades_permitidas"]:
        errores.append(f"Severidad no permitida: {riesgo.get('severidad')}")
    if riesgo.get("estado_control") not in config["estados_control_permitidos"]:
        errores.append(f"Estado de control no permitido: {riesgo.get('estado_control')}")
    if not isinstance(riesgo.get("controles_defensivos"), list) or not riesgo["controles_defensivos"]:
        errores.append("controles_defensivos debe ser una lista no vacía")
    for bandera in ("usa_datos_reales", "usa_ia_real", "usa_api_externa", "usa_cloud"):
        if riesgo.get(bandera) is not False:
            errores.append(f"{bandera} debe ser false")
    return errores


def calcular_puntuacion_riesgo(riesgo: dict[str, Any], config: dict[str, Any]) -> float:
    p = config["pesos_riesgo"]
    score = (
        float(riesgo["impacto_operativo_simulado"]) * p["impacto_operativo"]
        + float(riesgo["impacto_privacidad_simulado"]) * p["impacto_privacidad"]
        + float(riesgo["impacto_seguridad_simulado"]) * p["impacto_seguridad"]
        + float(riesgo["probabilidad_simulada"]) * p["probabilidad"]
    )
    if str(riesgo.get("detectabilidad", "")).lower() == "baja":
        score += p["detectabilidad_baja_bono"]
    score += SEVERIDAD_MAPA.get(str(riesgo.get("severidad", "")).lower(), 0) * 0.1
    return round(score, 2)


def asignar_nivel_riesgo(puntuacion: float, config: dict[str, Any]) -> str:
    u = config["umbrales_riesgo"]
    if puntuacion >= u["alto"]:
        return "critico"
    if puntuacion >= u["medio"]:
        return "alto"
    if puntuacion >= u["bajo"]:
        return "medio"
    return "bajo"


def inventariar_riesgos(riesgos: list[dict[str, Any]], config: dict[str, Any]) -> dict[str, Any]:
    errores: list[str] = []
    validados: list[dict[str, Any]] = []
    for riesgo in riesgos:
        err = validar_riesgo(riesgo, config)
        if err:
            errores.append(f"{riesgo.get('id_riesgo', 'SIN_ID')}: " + " | ".join(err))
            continue
        nuevo = dict(riesgo)
        nuevo["puntuacion_riesgo_simulada"] = calcular_puntuacion_riesgo(riesgo, config)
        nuevo["nivel_riesgo"] = asignar_nivel_riesgo(nuevo["puntuacion_riesgo_simulada"], config)
        validados.append(nuevo)

    criticos = [r for r in validados if r["nivel_riesgo"] == "critico"]
    baja_detectabilidad = [r for r in validados if r.get("detectabilidad") == "baja"]
    sin_controles = [r for r in validados if len(r.get("controles_defensivos", [])) < 2]

    return {
        "fecha_generacion": datetime.now().isoformat(timespec="seconds"),
        "total_riesgos_inventariados": len(validados),
        "errores_validacion": errores,
        "distribucion_por_categoria": dict(Counter(r["categoria"] for r in validados)),
        "distribucion_por_severidad": dict(Counter(r["severidad"] for r in validados)),
        "riesgos_criticos": criticos,
        "riesgos_baja_detectabilidad": baja_detectabilidad,
        "riesgos_sin_controles_suficientes": sin_controles,
        "controles_defensivos_recomendados": config["controles_defensivos_recomendados"],
        "riesgos": validados,
    }


def generar_markdown(resultado: dict[str, Any]) -> str:
    lineas = [
        "# Informe de Inventario Defensivo de Riesgos de Agentes",
        "",
        f"Fecha de generación: {resultado['fecha_generacion']}",
        "",
        "## Resumen ejecutivo",
        "Inventario local de riesgos sintéticos para evaluación defensiva de agentes de IA.",
        "",
        "## Total de riesgos inventariados",
        str(resultado["total_riesgos_inventariados"]),
        "",
        "## Distribución por categoría",
    ]
    lineas.extend([f"- {k}: {v}" for k, v in resultado["distribucion_por_categoria"].items()])
    lineas += ["", "## Distribución por severidad"]
    lineas.extend([f"- {k}: {v}" for k, v in resultado["distribucion_por_severidad"].items()])
    lineas += ["", "## Riesgos críticos"]
    if resultado["riesgos_criticos"]:
        lineas.extend(
            [
                f"- {r['id_riesgo']} - {r['nombre_riesgo']} (puntuación: {r['puntuacion_riesgo_simulada']})"
                for r in resultado["riesgos_criticos"]
            ]
        )
    else:
        lineas.append("- No se detectaron riesgos críticos.")
    lineas += ["", "## Riesgos con baja detectabilidad"]
    if resultado["riesgos_baja_detectabilidad"]:
        lineas.extend([f"- {r['id_riesgo']} - {r['nombre_riesgo']}" for r in resultado["riesgos_baja_detectabilidad"]])
    else:
        lineas.append("- No se detectaron riesgos con baja detectabilidad.")
    lineas += ["", "## Controles defensivos recomendados"]
    lineas.extend([f"- {c}" for c in resultado["controles_defensivos_recomendados"]])
    lineas += [
        "",
        "## Lectura técnica defensiva",
        "El inventario permite priorizar mitigaciones y reforzar revisión humana en riesgos críticos.",
        "",
        "## Límites del inventario",
        "Solo contempla escenarios sintéticos no accionables y no representa operación productiva.",
        "",
        "## Recomendaciones siguientes",
        "1. Reforzar controles en riesgos críticos y de baja detectabilidad.",
        "2. Ampliar evidencias de trazabilidad por riesgo.",
        "3. Revisar umbrales y pesos del modelo simulado.",
        "",
        "## 🪪 Licencia y Autoría",
        "Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  ",
        "© 2025 – Txema Ríos. Todos los derechos compartidos.",
    ]
    return "\n".join(lineas) + "\n"


def ejecutar(ruta_riesgos: Path, ruta_config: Path, salida_md: Path, salida_json: Path) -> dict[str, Any]:
    riesgos = cargar_json(ruta_riesgos)
    config = cargar_json(ruta_config)
    if not isinstance(riesgos, list):
        raise ValueError("El archivo de riesgos debe contener una lista JSON")
    if not isinstance(config, dict):
        raise ValueError("El archivo de configuración debe contener un objeto JSON")
    resultado = inventariar_riesgos(riesgos, config)
    salida_md.parent.mkdir(parents=True, exist_ok=True)
    salida_json.parent.mkdir(parents=True, exist_ok=True)
    salida_md.write_text(generar_markdown(resultado), encoding="utf-8")
    salida_json.write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8")
    return resultado


def main() -> None:
    parser = argparse.ArgumentParser(description="Inventario local defensivo de riesgos de agentes.")
    parser.add_argument("--risks", required=True, type=Path)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--output-md", required=True, type=Path)
    parser.add_argument("--output-json", required=True, type=Path)
    args = parser.parse_args()
    resultado = ejecutar(args.risks, args.config, args.output_md, args.output_json)
    print(f"Inventario generado. Riesgos válidos: {resultado['total_riesgos_inventariados']}")


if __name__ == "__main__":
    main()
