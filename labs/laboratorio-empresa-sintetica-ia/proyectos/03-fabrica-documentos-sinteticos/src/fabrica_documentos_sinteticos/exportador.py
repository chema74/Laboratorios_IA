"""Exportación de documentos sintéticos en Markdown y JSON."""

from __future__ import annotations

import json
from pathlib import Path


def _asegurar_carpeta(ruta: Path) -> None:
    ruta.mkdir(parents=True, exist_ok=True)


def exportar_documentos(documentos: list[dict], resumen: dict, ruta_salida: str | Path) -> dict[str, str]:
    """
    1) Crea carpeta de salida y subcarpetas por tipo.
    2) Escribe archivos Markdown por documento.
    3) Genera índice y resumen en JSON.
    """
    salida = Path(ruta_salida)
    _asegurar_carpeta(salida)

    for doc in documentos:
        ruta_md = salida / doc["ruta_markdown"]
        _asegurar_carpeta(ruta_md.parent)
        ruta_md.write_text(doc["contenido_markdown"], encoding="utf-8")

    indice = []
    for doc in documentos:
        copia = {k: v for k, v in doc.items() if k != "contenido_markdown"}
        indice.append(copia)

    ruta_indice = salida / "indice_documentos.json"
    ruta_resumen = salida / "resumen_documentos.json"

    ruta_indice.write_text(json.dumps(indice, ensure_ascii=False, indent=2), encoding="utf-8")
    ruta_resumen.write_text(json.dumps(resumen, ensure_ascii=False, indent=2), encoding="utf-8")

    return {
        "indice_documentos": str(ruta_indice),
        "resumen_documentos": str(ruta_resumen),
    }
