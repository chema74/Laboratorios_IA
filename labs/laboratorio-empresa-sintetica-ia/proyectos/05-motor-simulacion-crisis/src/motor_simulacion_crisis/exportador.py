"""Exportador de crisis simuladas y artefactos asociados."""

from __future__ import annotations

import csv
import json
from pathlib import Path


def _asegurar(ruta: Path) -> None:
    ruta.mkdir(parents=True, exist_ok=True)


def _exportar_csv(datos: list[dict], ruta: Path) -> None:
    if not datos:
        ruta.write_text("", encoding="utf-8")
        return
    campos = list(datos[0].keys())
    with ruta.open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(datos)


def exportar_resultados_crisis(
    crisis: list[dict],
    linea_tiempo: list[dict],
    resumen: dict,
    expediente_markdown: str,
    ruta_salida: str | Path,
) -> dict[str, str]:
    """
    1) Crea carpeta salida si no existe.
    2) Exporta JSON/CSV de crisis y línea temporal.
    3) Exporta resumen JSON y expediente Markdown.
    """
    salida = Path(ruta_salida)
    _asegurar(salida)

    ruta_crisis_json = salida / "crisis_simuladas.json"
    ruta_crisis_csv = salida / "crisis_simuladas.csv"
    ruta_linea_json = salida / "linea_tiempo_crisis.json"
    ruta_linea_csv = salida / "linea_tiempo_crisis.csv"
    ruta_resumen = salida / "resumen_crisis.json"
    ruta_expediente = salida / "expediente_crisis.md"

    ruta_crisis_json.write_text(json.dumps(crisis, ensure_ascii=False, indent=2), encoding="utf-8")
    ruta_linea_json.write_text(json.dumps(linea_tiempo, ensure_ascii=False, indent=2), encoding="utf-8")
    ruta_resumen.write_text(json.dumps(resumen, ensure_ascii=False, indent=2), encoding="utf-8")
    ruta_expediente.write_text(expediente_markdown, encoding="utf-8")

    _exportar_csv(crisis, ruta_crisis_csv)
    _exportar_csv(linea_tiempo, ruta_linea_csv)

    return {
        "crisis_json": str(ruta_crisis_json),
        "crisis_csv": str(ruta_crisis_csv),
        "linea_json": str(ruta_linea_json),
        "linea_csv": str(ruta_linea_csv),
        "resumen_json": str(ruta_resumen),
        "expediente_md": str(ruta_expediente),
    }
