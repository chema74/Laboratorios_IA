"""Simulador local de analítica tipo Sheets con IA simulada."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from statistics import mean


def cargar_config(ruta: Path) -> dict:
    with ruta.open("r", encoding="utf-8-sig") as archivo:
        return json.load(archivo)


def cargar_csv(ruta: Path) -> list[dict]:
    with ruta.open("r", encoding="utf-8-sig", newline="") as archivo:
        return list(csv.DictReader(archivo))


def validar_columnas(registros: list[dict], columnas_esperadas: list[str]) -> None:
    if not registros:
        raise ValueError("No hay registros en la hoja sintética.")
    columnas = set(registros[0].keys())
    faltantes = set(columnas_esperadas).difference(columnas)
    if faltantes:
        raise ValueError(f"Faltan columnas: {sorted(faltantes)}")


def to_float(valor: str) -> float:
    return float(valor.strip())


def calcular_indicadores(registros: list[dict]) -> dict:
    importe_total = sum(to_float(x["importe_simulado"]) for x in registros)
    coste_total = sum(to_float(x["coste_simulado"]) for x in registros)
    margen_total = sum(to_float(x["margen_simulado"]) for x in registros)
    margen_porcentual = (margen_total / importe_total * 100.0) if importe_total else 0.0
    margen_promedio = mean(to_float(x["margen_simulado"]) for x in registros)
    return {
        "total_registros": len(registros),
        "importe_total_simulado": round(importe_total, 2),
        "coste_total_simulado": round(coste_total, 2),
        "margen_total_simulado": round(margen_total, 2),
        "margen_porcentual_simulado": round(margen_porcentual, 2),
        "margen_promedio_simulado": round(margen_promedio, 2),
    }


def calcular_distribuciones(registros: list[dict]) -> dict:
    return {
        "por_area_negocio": dict(Counter(x["area_negocio"] for x in registros)),
        "por_canal": dict(Counter(x["canal"] for x in registros)),
        "por_estado": dict(Counter(x["estado_operacion"] for x in registros)),
        "por_prioridad": dict(Counter(x["prioridad"] for x in registros)),
    }


def detectar_senales(registros: list[dict], config: dict) -> list[str]:
    umbral_margen = config["reglas_alertas"]["umbral_margen_bajo"]
    prioridad_alta = config["reglas_alertas"]["prioridad_alta"]
    margen_bajo = [x["id_registro"] for x in registros if to_float(x["margen_simulado"]) < umbral_margen]
    alta_prioridad = [x["id_registro"] for x in registros if x["prioridad"] == prioridad_alta]
    senales = []
    if margen_bajo:
        senales.append(f"Registros con margen bajo (<{umbral_margen}): {', '.join(margen_bajo[:6])}")
    if alta_prioridad:
        senales.append(f"Registros de prioridad alta: {len(alta_prioridad)}")
    pendientes = [x["id_registro"] for x in registros if x["estado_operacion"] == "Pendiente"]
    if pendientes:
        senales.append(f"Registros pendientes: {len(pendientes)}")
    return senales


def generar_resumen_ejecutivo(indicadores: dict, distribuciones: dict) -> str:
    area_top = max(distribuciones["por_area_negocio"], key=distribuciones["por_area_negocio"].get)
    estado_top = max(distribuciones["por_estado"], key=distribuciones["por_estado"].get)
    return (
        f"Se procesaron {indicadores['total_registros']} registros sintéticos. "
        f"Margen total simulado: {indicadores['margen_total_simulado']}. "
        f"Área con mayor volumen: {area_top}. Estado dominante: {estado_top}."
    )


def guardar_hoja_enriquecida(registros: list[dict], sheets_dir: Path) -> str:
    sheets_dir.mkdir(parents=True, exist_ok=True)
    salida = sheets_dir / "hoja_enriquecida_simulada.csv"
    columnas = list(registros[0].keys()) + ["alerta_margen_bajo", "alerta_prioridad_alta"]
    with salida.open("w", encoding="utf-8", newline="") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=columnas)
        writer.writeheader()
        for fila in registros:
            margen_bajo = "si" if to_float(fila["margen_simulado"]) < 150 else "no"
            alta = "si" if fila["prioridad"] == "Alta" else "no"
            writer.writerow({**fila, "alerta_margen_bajo": margen_bajo, "alerta_prioridad_alta": alta})
    return str(salida)


def construir_resultado(registros: list[dict], config: dict, hoja_enriquecida: str) -> dict:
    indicadores = calcular_indicadores(registros)
    distribuciones = calcular_distribuciones(registros)
    revision = [x["id_registro"] for x in registros if x["requiere_revision"].lower() == config["reglas_revision"]["valor_revision"]]
    senales = detectar_senales(registros, config)
    resumen = generar_resumen_ejecutivo(indicadores, distribuciones)
    return {
        "fecha_generacion": datetime.now().isoformat(timespec="seconds"),
        "indicadores_operativos": {"total_registros": indicadores["total_registros"], "registros_revision": len(revision)},
        "indicadores_financieros_simulados": {
            "importe_total_simulado": indicadores["importe_total_simulado"],
            "coste_total_simulado": indicadores["coste_total_simulado"],
            "margen_total_simulado": indicadores["margen_total_simulado"],
            "margen_porcentual_simulado": indicadores["margen_porcentual_simulado"],
            "margen_promedio_simulado": indicadores["margen_promedio_simulado"],
            "moneda_simulada": config["moneda_simulada"],
        },
        "distribuciones": distribuciones,
        "señales_analiticas_simuladas": senales,
        "resumen_ejecutivo_simulado": resumen,
        "registros_revision": revision,
        "hoja_enriquecida_generada": hoja_enriquecida,
        "usa_sheets_real": False,
        "usa_oauth_real": False,
        "usa_api_externa": False,
        "usa_cloud": False,
        "usa_ia_real": False,
        "nota": config["nota"],
    }


def generar_informe_markdown(resultado: dict, output_md: Path) -> None:
    lineas = [
        "# Informe de Simulación Sheets IA Analítica (Local)",
        "",
        f"**Fecha de generación:** {resultado['fecha_generacion']}",
        "",
        "## Resumen ejecutivo",
        resultado["resumen_ejecutivo_simulado"],
        "",
        "## Total de registros",
        f"- {resultado['indicadores_operativos']['total_registros']}",
        "",
        "## Indicadores financieros simulados",
    ]
    for k, v in resultado["indicadores_financieros_simulados"].items():
        lineas.append(f"- {k}: {v}")
    lineas.extend(["", "## Distribución por área"])
    for k, v in resultado["distribuciones"]["por_area_negocio"].items():
        lineas.append(f"- {k}: {v}")
    lineas.extend(["", "## Distribución por canal"])
    for k, v in resultado["distribuciones"]["por_canal"].items():
        lineas.append(f"- {k}: {v}")
    lineas.extend(["", "## Distribución por estado"])
    for k, v in resultado["distribuciones"]["por_estado"].items():
        lineas.append(f"- {k}: {v}")
    lineas.extend(["", "## Señales analíticas simuladas"])
    for s in resultado["señales_analiticas_simuladas"]:
        lineas.append(f"- {s}")
    lineas.extend(["", "## Registros que requieren revisión"])
    for r in resultado["registros_revision"][:10]:
        lineas.append(f"- {r}")
    lineas.extend(
        [
            "",
            "## Hoja enriquecida generada",
            f"- {resultado['hoja_enriquecida_generada']}",
            "",
            "## Límites de la simulación",
            "Sin Sheets real, sin OAuth real, sin APIs externas, sin Google Cloud y sin IA real.",
            "",
            "## Recomendaciones siguientes",
            "1. Incrementar reglas de alertas por área.",
            "2. Cruzar métricas con simuladores 02 y 03.",
            "3. Definir conector V2 opcional por `.env` con fallback local.",
            "",
            "## 🪪 Licencia y Autoría",
            "Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  ",
            "© 2025 – Txema Ríos. Todos los derechos compartidos.",
        ]
    )
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text("\n".join(lineas), encoding="utf-8")


def parsear_argumentos() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Simulador local de Sheets IA analítica")
    parser.add_argument("--sheet", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output-md", required=True)
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--sheets-dir", required=True)
    return parser.parse_args()


def main() -> None:
    args = parsear_argumentos()
    registros = cargar_csv(Path(args.sheet))
    config = cargar_config(Path(args.config))
    validar_columnas(registros, config["columnas_esperadas"])
    hoja_enriquecida = guardar_hoja_enriquecida(registros, Path(args.sheets_dir))
    resultado = construir_resultado(registros, config, hoja_enriquecida)
    output_json = Path(args.output_json)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8")
    generar_informe_markdown(resultado, Path(args.output_md))


if __name__ == "__main__":
    main()
