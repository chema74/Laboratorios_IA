"""Utilidades de exportación para la empresa sintética."""

from __future__ import annotations

import csv
import json
from pathlib import Path


def asegurar_carpeta_salida(ruta_salida: str | Path) -> Path:
    ruta = Path(ruta_salida)
    ruta.mkdir(parents=True, exist_ok=True)
    return ruta


def exportar_empresa_json(empresa: dict, ruta_salida: str | Path, nombre_archivo: str = "empresa_sintetica.json") -> Path:
    carpeta = asegurar_carpeta_salida(ruta_salida)
    destino = carpeta / nombre_archivo
    with destino.open("w", encoding="utf-8") as archivo:
        json.dump(empresa, archivo, ensure_ascii=False, indent=2)
    return destino


def _exportar_lista_csv(filas: list[dict], ruta_archivo: Path) -> None:
    if not filas:
        with ruta_archivo.open("w", newline="", encoding="utf-8") as archivo:
            archivo.write("")
        return

    campos = list(filas[0].keys())
    with ruta_archivo.open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(filas)


def exportar_tablas_csv(empresa: dict, ruta_salida: str | Path) -> list[Path]:
    carpeta = asegurar_carpeta_salida(ruta_salida)
    exportaciones = {
        "empleados": empresa.get("empleados", []),
        "clientes": empresa.get("clientes", []),
        "productos": empresa.get("productos", []),
        "procesos": empresa.get("procesos", []),
    }

    rutas: list[Path] = []
    for nombre, filas in exportaciones.items():
        ruta = carpeta / f"{nombre}.csv"
        _exportar_lista_csv(filas, ruta)
        rutas.append(ruta)
    return rutas
