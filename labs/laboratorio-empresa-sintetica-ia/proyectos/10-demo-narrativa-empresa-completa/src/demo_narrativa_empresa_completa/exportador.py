"""Exportación de artefactos de la demo narrativa."""

from __future__ import annotations

import csv
import json
from pathlib import Path


def _asegurar_directorio(ruta: Path) -> None:
    ruta.mkdir(parents=True, exist_ok=True)


def _exportar_json(ruta: Path, data: object) -> None:
    ruta.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _exportar_csv(ruta: Path, filas: list[dict]) -> None:
    if not filas:
        ruta.write_text("", encoding="utf-8")
        return
    normalizadas: list[dict] = []
    for fila in filas:
        flat = {}
        for clave, valor in fila.items():
            flat[clave] = json.dumps(valor, ensure_ascii=False) if isinstance(valor, (dict, list)) else valor
        normalizadas.append(flat)
    headers = list(normalizadas[0].keys())
    with ruta.open("w", newline="", encoding="utf-8") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=headers)
        writer.writeheader()
        writer.writerows(normalizadas)


def exportar_demo_narrativa(
    narrativa: dict,
    guion_md: str,
    expediente_md: str,
    salida: str | Path,
) -> dict[str, str]:
    out = Path(salida)
    _asegurar_directorio(out)

    rutas = {
        "demo_json": out / "demo_narrativa_empresa_completa.json",
        "linea_tiempo_json": out / "linea_tiempo_semanal.json",
        "linea_tiempo_csv": out / "linea_tiempo_semanal.csv",
        "episodios_json": out / "episodios_narrativos.json",
        "episodios_csv": out / "episodios_narrativos.csv",
        "mapa_evidencias_json": out / "mapa_evidencias.json",
        "mapa_evidencias_csv": out / "mapa_evidencias.csv",
        "resumen_json": out / "resumen_demo_narrativa.json",
        "guion_md": out / "guion_demo.md",
        "expediente_md": out / "expediente_demo_empresa_completa.md",
    }

    _exportar_json(rutas["demo_json"], narrativa)
    _exportar_json(rutas["linea_tiempo_json"], narrativa["linea_tiempo_semanal"])
    _exportar_json(rutas["episodios_json"], narrativa["episodios_narrativos"])
    _exportar_json(rutas["mapa_evidencias_json"], narrativa["mapa_evidencias"])
    _exportar_json(rutas["resumen_json"], narrativa["resumen_demo_narrativa"])
    rutas["guion_md"].write_text(guion_md, encoding="utf-8")
    rutas["expediente_md"].write_text(expediente_md, encoding="utf-8")

    _exportar_csv(rutas["linea_tiempo_csv"], narrativa["linea_tiempo_semanal"])
    _exportar_csv(rutas["episodios_csv"], narrativa["episodios_narrativos"])
    _exportar_csv(rutas["mapa_evidencias_csv"], narrativa["mapa_evidencias"])

    return {k: str(v) for k, v in rutas.items()}

