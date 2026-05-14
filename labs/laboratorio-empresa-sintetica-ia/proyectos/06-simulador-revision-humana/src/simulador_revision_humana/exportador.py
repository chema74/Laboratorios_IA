"""Exportación de revisiones, registros, resumen y expediente."""

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


def exportar_resultados_revision(
    revisiones: list[dict],
    registros: list[dict],
    resumen: dict,
    expediente_markdown: str,
    ruta_salida: str | Path,
) -> dict[str, str]:
    """
    1) Crea carpeta de salida.
    2) Exporta JSON/CSV de revisiones y registros.
    3) Exporta resumen JSON y expediente Markdown.
    """
    salida = Path(ruta_salida)
    _asegurar(salida)

    ruta_rev_json = salida / "revisiones_humanas.json"
    ruta_rev_csv = salida / "revisiones_humanas.csv"
    ruta_reg_json = salida / "registro_decisiones.json"
    ruta_reg_csv = salida / "registro_decisiones.csv"
    ruta_resumen = salida / "resumen_revision_humana.json"
    ruta_expediente = salida / "expediente_revision_humana.md"

    ruta_rev_json.write_text(json.dumps(revisiones, ensure_ascii=False, indent=2), encoding="utf-8")
    ruta_reg_json.write_text(json.dumps(registros, ensure_ascii=False, indent=2), encoding="utf-8")
    ruta_resumen.write_text(json.dumps(resumen, ensure_ascii=False, indent=2), encoding="utf-8")
    ruta_expediente.write_text(expediente_markdown, encoding="utf-8")

    _exportar_csv(revisiones, ruta_rev_csv)
    _exportar_csv(registros, ruta_reg_csv)

    return {
        "revisiones_json": str(ruta_rev_json),
        "revisiones_csv": str(ruta_rev_csv),
        "registro_json": str(ruta_reg_json),
        "registro_csv": str(ruta_reg_csv),
        "resumen_json": str(ruta_resumen),
        "expediente_md": str(ruta_expediente),
    }
