"""Exportación de escenarios en JSON, CSV y Markdown."""

from __future__ import annotations

import csv
import json
from pathlib import Path


def _asegurar(ruta: Path) -> None:
    ruta.mkdir(parents=True, exist_ok=True)


def _markdown_escenario(esc: dict) -> str:
    return (
        f"# {esc['titulo']}\n\n"
        "**Aviso:** Escenario sintético de prueba. No ejecuta agentes reales ni usa datos reales.\n\n"
        "## Metadatos\n"
        f"- id_escenario: {esc['id_escenario']}\n"
        f"- tipo_escenario: {esc['tipo_escenario']}\n"
        f"- nivel_dificultad: {esc['nivel_dificultad']}\n"
        f"- accion_recomendada: {esc['accion_recomendada']}\n"
        f"- requiere_revision_humana: {esc['requiere_revision_humana']}\n"
        f"- origen_simulado: {esc['origen_simulado']}\n\n"
        "## Descripción\n"
        f"{esc['descripcion']}\n\n"
        "## Entrada simulada\n"
        f"{esc['entrada_usuario_simulada']}\n\n"
        "## Comportamiento esperado\n"
        f"{esc['comportamiento_esperado']}\n\n"
        "## Criterio de evaluación\n"
        f"{esc['criterio_evaluacion']}\n"
    )


def exportar_escenarios(escenarios: list[dict], resumen: dict, ruta_salida: str | Path) -> dict[str, str]:
    """
    1) Crea carpeta de salida y subcarpeta markdown.
    2) Exporta JSON/CSV/Resumen.
    3) Exporta un .md por escenario.
    """
    salida = Path(ruta_salida)
    markdown_dir = salida / "escenarios_markdown"
    _asegurar(salida)
    _asegurar(markdown_dir)

    ruta_json = salida / "escenarios_prueba_agentes.json"
    ruta_csv = salida / "escenarios_prueba_agentes.csv"
    ruta_resumen = salida / "resumen_escenarios.json"

    ruta_json.write_text(json.dumps(escenarios, ensure_ascii=False, indent=2), encoding="utf-8")
    ruta_resumen.write_text(json.dumps(resumen, ensure_ascii=False, indent=2), encoding="utf-8")

    if escenarios:
        campos = list(escenarios[0].keys())
        with ruta_csv.open("w", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=campos)
            escritor.writeheader()
            escritor.writerows(escenarios)
    else:
        ruta_csv.write_text("", encoding="utf-8")

    for esc in escenarios:
        (markdown_dir / f"{esc['id_escenario']}.md").write_text(_markdown_escenario(esc), encoding="utf-8")

    return {
        "escenarios_json": str(ruta_json),
        "escenarios_csv": str(ruta_csv),
        "resumen_json": str(ruta_resumen),
        "markdown_dir": str(markdown_dir),
    }
