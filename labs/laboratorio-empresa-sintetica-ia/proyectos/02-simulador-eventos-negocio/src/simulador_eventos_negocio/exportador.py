"""Exportadores de eventos y resumen."""

from __future__ import annotations

import csv
import json
from pathlib import Path


def asegurar_carpeta_salida(ruta_salida: str | Path) -> Path:
    ruta = Path(ruta_salida)
    ruta.mkdir(parents=True, exist_ok=True)
    return ruta


def exportar_eventos_json_csv(eventos: list[dict], ruta_salida: str | Path) -> tuple[Path, Path]:
    carpeta = asegurar_carpeta_salida(ruta_salida)
    ruta_json = carpeta / "eventos_negocio.json"
    ruta_csv = carpeta / "eventos_negocio.csv"

    with ruta_json.open("w", encoding="utf-8") as archivo:
        json.dump(eventos, archivo, ensure_ascii=False, indent=2)

    if eventos:
        campos = list(eventos[0].keys())
        with ruta_csv.open("w", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=campos)
            escritor.writeheader()
            escritor.writerows(eventos)
    else:
        ruta_csv.write_text("", encoding="utf-8")

    return ruta_json, ruta_csv


def exportar_resumen_json(resumen: dict, ruta_salida: str | Path) -> Path:
    carpeta = asegurar_carpeta_salida(ruta_salida)
    ruta = carpeta / "resumen_eventos.json"
    with ruta.open("w", encoding="utf-8") as archivo:
        json.dump(resumen, archivo, ensure_ascii=False, indent=2)
    return ruta
