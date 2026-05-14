import argparse
import csv
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from statistics import mean


def cargar_config(ruta: Path) -> dict:
    with ruta.open("r", encoding="utf-8") as f:
        return json.load(f)


def cargar_csv(ruta: Path) -> list[dict]:
    with ruta.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def validar_columnas(registros: list[dict], columnas_esperadas: list[str]) -> None:
    if not registros:
        raise ValueError("El CSV no contiene registros.")
    columnas = set(registros[0].keys())
    faltantes = [c for c in columnas_esperadas if c not in columnas]
    if faltantes:
        raise ValueError(f"Faltan columnas esperadas: {faltantes}")


def a_float(valor: str) -> float:
    return float(str(valor).strip().replace(",", "."))


def calcular_indicadores(registros: list[dict], config: dict) -> dict:
    importes = [a_float(r["importe_simulado"]) for r in registros]
    costes = [a_float(r["coste_simulado"]) for r in registros]
    margenes = [a_float(r["margen_simulado"]) for r in registros]
    total_importe = sum(importes)
    total_coste = sum(costes)
    total_margen = sum(margenes)
    margen_pct = (total_margen / total_importe * 100.0) if total_importe else 0.0

    por_area = dict(Counter(r["area_negocio"] for r in registros))
    por_canal = dict(Counter(r["canal"] for r in registros))
    por_estado = dict(Counter(r["estado_operacion"] for r in registros))

    valores_revision = {v.lower() for v in config["reglas_revision"]["valores_positivos"]}
    registros_revision = [r for r in registros if str(r["requiere_revision"]).lower() in valores_revision]
    prioridad_alta = config["reglas_indicadores"]["prioridad_alta"].lower()
    prioridades_altas = [r for r in registros if str(r["prioridad"]).lower() == prioridad_alta]
    ratio_revision = len(registros_revision) / len(registros)

    alertas = []
    if margen_pct < float(config["reglas_alertas"]["margen_porcentual_minimo"]):
        alertas.append("Margen porcentual por debajo del umbral configurado.")
    if ratio_revision > float(config["reglas_alertas"]["ratio_revision_maximo"]):
        alertas.append("Proporción de revisión superior al máximo configurado.")
    if not alertas:
        alertas.append("Sin alertas críticas en esta simulación.")

    resumen = [
        f"Total registros: {len(registros)}.",
        f"Importe total simulado: {total_importe:.2f} {config['moneda_simulada']}.",
        f"Margen porcentual simulado: {margen_pct:.2f}%.",
        f"Registros con revisión: {len(registros_revision)}.",
    ][: int(config["reglas_resumen_ejecutivo"]["max_lineas"])]

    return {
        "indicadores_operativos": {
            "total_registros": len(registros),
            "registros_revision": len(registros_revision),
            "prioridades_altas": len(prioridades_altas),
            "importe_promedio_simulado": round(mean(importes), 2),
        },
        "indicadores_financieros_simulados": {
            "importe_total_simulado": round(total_importe, 2),
            "coste_total_simulado": round(total_coste, 2),
            "margen_total_simulado": round(total_margen, 2),
            "margen_porcentual_simulado": round(margen_pct, 2),
        },
        "distribuciones": {
            "por_area_negocio": por_area,
            "por_canal": por_canal,
            "por_estado_operacion": por_estado,
        },
        "señales_analiticas_simuladas": alertas,
        "resumen_ejecutivo_simulado": " ".join(resumen),
        "registros_revision": [r["id_registro"] for r in registros_revision],
    }


def guardar_libro_enriquecido(workbooks_dir: Path, registros: list[dict]) -> str:
    workbooks_dir.mkdir(parents=True, exist_ok=True)
    salida = workbooks_dir / "libro_excel_operativo_enriquecido.csv"
    campos = list(registros[0].keys()) + ["alerta_revision"]
    with salida.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        for r in registros:
            fila = dict(r)
            fila["alerta_revision"] = "si" if str(r["requiere_revision"]).lower() in {"si", "true", "1"} else "no"
            writer.writerow(fila)
    return str(salida)


def generar_informe_md(resultado: dict, libro_enriquecido: str, moneda: str) -> str:
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dist = resultado["distribuciones"]
    fin = resultado["indicadores_financieros_simulados"]
    md = [
        "# Informe Simulador Excel IA Analítica (V1 Local)",
        "",
        f"Fecha de generación: {fecha}",
        "",
        "## Resumen ejecutivo",
        resultado["resumen_ejecutivo_simulado"],
        "",
        "## Total de registros",
        f"- {resultado['indicadores_operativos']['total_registros']}",
        "",
        "## Indicadores financieros simulados",
        f"- Importe total simulado: {fin['importe_total_simulado']} {moneda}",
        f"- Coste total simulado: {fin['coste_total_simulado']} {moneda}",
        f"- Margen total simulado: {fin['margen_total_simulado']} {moneda}",
        f"- Margen porcentual simulado: {fin['margen_porcentual_simulado']}%",
        "",
        "## Distribución por área",
    ]
    for k in sorted(dist["por_area_negocio"]):
        md.append(f"- {k}: {dist['por_area_negocio'][k]}")
    md.extend(["", "## Distribución por canal"])
    for k in sorted(dist["por_canal"]):
        md.append(f"- {k}: {dist['por_canal'][k]}")
    md.extend(["", "## Distribución por estado"])
    for k in sorted(dist["por_estado_operacion"]):
        md.append(f"- {k}: {dist['por_estado_operacion'][k]}")
    md.extend(["", "## Señales analíticas simuladas"])
    for alerta in resultado["señales_analiticas_simuladas"]:
        md.append(f"- {alerta}")
    md.extend(
        [
            "",
            "## Registros que requieren revisión",
            "- " + ", ".join(resultado["registros_revision"]) if resultado["registros_revision"] else "- Ninguno",
            "",
            "## Libro enriquecido generado",
            f"- {libro_enriquecido}",
            "",
            "## Límites de la simulación",
            "- Sin Excel real.",
            "- Sin Microsoft Graph API real.",
            "- Sin OAuth real.",
            "- Sin Azure obligatorio.",
            "- Sin IA real ni datos reales.",
            "",
            "## Recomendaciones siguientes",
            "- Ajustar umbrales de alertas simuladas por área de negocio.",
            "- Versionar reglas de revisión y priorización.",
            "- Mantener integración V2 opcional vía .env con fallback local.",
            "",
            "## 🪪 Licencia y Autoría",
            "Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  ",
            "© 2025 – Txema Ríos. Todos los derechos compartidos.",
            "",
        ]
    )
    return "\n".join(md)


def ejecutar(workbook_path: Path, config_path: Path, output_md: Path, output_json: Path, workbooks_dir: Path) -> dict:
    config = cargar_config(config_path)
    registros = cargar_csv(workbook_path)
    validar_columnas(registros, config["columnas_esperadas"])
    resultado = calcular_indicadores(registros, config)
    libro_enriquecido = guardar_libro_enriquecido(workbooks_dir, registros)
    resultado["libro_enriquecido_generado"] = libro_enriquecido
    resultado.update(
        {
            "usa_excel_real": False,
            "usa_microsoft_graph_real": False,
            "usa_oauth_real": False,
            "usa_api_externa": False,
            "usa_azure": False,
            "usa_ia_real": False,
        }
    )

    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(generar_informe_md(resultado, libro_enriquecido, config["moneda_simulada"]), encoding="utf-8")
    output_json.write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8")
    return resultado


def crear_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Simulador local de Excel con analítica IA simulada.")
    parser.add_argument("--workbook", required=True, type=Path)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--output-md", required=True, type=Path)
    parser.add_argument("--output-json", required=True, type=Path)
    parser.add_argument("--workbooks-dir", required=True, type=Path)
    return parser


def main() -> None:
    args = crear_parser().parse_args()
    ejecutar(args.workbook, args.config, args.output_md, args.output_json, args.workbooks_dir)


if __name__ == "__main__":
    main()
