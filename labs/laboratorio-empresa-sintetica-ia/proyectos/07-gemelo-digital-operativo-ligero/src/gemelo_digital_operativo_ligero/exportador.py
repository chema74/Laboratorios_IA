"""Exportación de artefactos del gemelo digital operativo."""

from __future__ import annotations

import csv
import json
from pathlib import Path


def _asegurar(ruta: Path) -> None:
    ruta.mkdir(parents=True, exist_ok=True)


def _exportar_csv_filas(filas: list[dict], ruta: Path) -> None:
    if not filas:
        ruta.write_text("", encoding="utf-8")
        return
    campos = list(filas[0].keys())
    with ruta.open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(filas)


def exportar_gemelo_digital(
    estado: dict,
    consecuencias: list[dict],
    resumen: dict,
    expediente: str,
    ruta_salida: str | Path,
) -> dict[str, str]:
    """
    1) Crea carpeta salida.
    2) Exporta JSON/CSV de métricas, alertas y decisiones.
    3) Exporta estado completo, consecuencias, línea temporal, resumen y expediente.
    """
    salida = Path(ruta_salida)
    _asegurar(salida)

    ruta_estado = salida / "estado_operativo.json"
    ruta_metricas_json = salida / "metricas_operativas.json"
    ruta_metricas_csv = salida / "metricas_operativas.csv"
    ruta_alertas_json = salida / "alertas_operativas.json"
    ruta_alertas_csv = salida / "alertas_operativas.csv"
    ruta_decisiones_json = salida / "decisiones_simuladas.json"
    ruta_decisiones_csv = salida / "decisiones_simuladas.csv"
    ruta_consecuencias_json = salida / "consecuencias_operativas.json"
    ruta_linea_json = salida / "linea_tiempo_operativa.json"
    ruta_resumen_json = salida / "resumen_gemelo_digital.json"
    ruta_expediente_md = salida / "expediente_estado_operativo.md"

    ruta_estado.write_text(json.dumps(estado, ensure_ascii=False, indent=2), encoding="utf-8")
    ruta_metricas_json.write_text(json.dumps(estado["metricas_operativas"], ensure_ascii=False, indent=2), encoding="utf-8")
    ruta_alertas_json.write_text(json.dumps(estado["alertas_operativas"], ensure_ascii=False, indent=2), encoding="utf-8")
    ruta_decisiones_json.write_text(json.dumps(estado["decisiones_simuladas"], ensure_ascii=False, indent=2), encoding="utf-8")
    ruta_consecuencias_json.write_text(json.dumps(consecuencias, ensure_ascii=False, indent=2), encoding="utf-8")
    ruta_linea_json.write_text(json.dumps(estado["linea_tiempo_operativa"], ensure_ascii=False, indent=2), encoding="utf-8")
    ruta_resumen_json.write_text(json.dumps(resumen, ensure_ascii=False, indent=2), encoding="utf-8")
    ruta_expediente_md.write_text(expediente, encoding="utf-8")

    _exportar_csv_filas([estado["metricas_operativas"]], ruta_metricas_csv)
    _exportar_csv_filas(estado["alertas_operativas"], ruta_alertas_csv)
    _exportar_csv_filas(estado["decisiones_simuladas"], ruta_decisiones_csv)

    return {
        "estado_operativo": str(ruta_estado),
        "metricas_json": str(ruta_metricas_json),
        "metricas_csv": str(ruta_metricas_csv),
        "alertas_json": str(ruta_alertas_json),
        "alertas_csv": str(ruta_alertas_csv),
        "decisiones_json": str(ruta_decisiones_json),
        "decisiones_csv": str(ruta_decisiones_csv),
        "consecuencias_json": str(ruta_consecuencias_json),
        "linea_tiempo_json": str(ruta_linea_json),
        "resumen_json": str(ruta_resumen_json),
        "expediente_md": str(ruta_expediente_md),
    }
