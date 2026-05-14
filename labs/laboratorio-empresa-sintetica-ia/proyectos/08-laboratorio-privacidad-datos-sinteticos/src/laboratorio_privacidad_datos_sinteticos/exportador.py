"""Exportación de artefactos del laboratorio de privacidad sintética."""

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


def exportar_resultados(
    inventario: list[dict],
    clasificacion: list[dict],
    matriz_permisos: list[dict],
    dataset_minimizado: dict,
    dataset_anonimizado: dict,
    riesgos: list[dict],
    resumen: dict,
    expediente: str,
    salida: str | Path,
) -> dict[str, str]:
    """Exporta JSON/CSV requeridos por la V1."""
    carpeta = Path(salida)
    _asegurar(carpeta)

    rutas = {
        "inventario_json": carpeta / "inventario_datos_sinteticos.json",
        "inventario_csv": carpeta / "inventario_datos_sinteticos.csv",
        "clasificacion_json": carpeta / "clasificacion_sensibilidad.json",
        "clasificacion_csv": carpeta / "clasificacion_sensibilidad.csv",
        "matriz_json": carpeta / "matriz_permisos_simulados.json",
        "matriz_csv": carpeta / "matriz_permisos_simulados.csv",
        "minimizado_json": carpeta / "dataset_minimizado_demo.json",
        "anonimizado_json": carpeta / "dataset_anonimizado_demo.json",
        "riesgos_json": carpeta / "riesgos_privacidad_simulados.json",
        "riesgos_csv": carpeta / "riesgos_privacidad_simulados.csv",
        "resumen_json": carpeta / "resumen_privacidad_datos_sinteticos.json",
        "expediente_md": carpeta / "expediente_privacidad_datos_sinteticos.md",
    }

    rutas["inventario_json"].write_text(json.dumps(inventario, ensure_ascii=False, indent=2), encoding="utf-8")
    rutas["clasificacion_json"].write_text(json.dumps(clasificacion, ensure_ascii=False, indent=2), encoding="utf-8")
    rutas["matriz_json"].write_text(json.dumps(matriz_permisos, ensure_ascii=False, indent=2), encoding="utf-8")
    rutas["minimizado_json"].write_text(json.dumps(dataset_minimizado, ensure_ascii=False, indent=2), encoding="utf-8")
    rutas["anonimizado_json"].write_text(json.dumps(dataset_anonimizado, ensure_ascii=False, indent=2), encoding="utf-8")
    rutas["riesgos_json"].write_text(json.dumps(riesgos, ensure_ascii=False, indent=2), encoding="utf-8")
    rutas["resumen_json"].write_text(json.dumps(resumen, ensure_ascii=False, indent=2), encoding="utf-8")
    rutas["expediente_md"].write_text(expediente, encoding="utf-8")

    _exportar_csv(inventario, rutas["inventario_csv"])
    _exportar_csv(clasificacion, rutas["clasificacion_csv"])
    _exportar_csv(matriz_permisos, rutas["matriz_csv"])
    _exportar_csv(riesgos, rutas["riesgos_csv"])

    return {k: str(v) for k, v in rutas.items()}
