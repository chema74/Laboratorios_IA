"""Exportación de resultados del comparador agente-proceso."""

from __future__ import annotations

import csv
import json
from pathlib import Path


def _asegurar(ruta: Path) -> None:
    ruta.mkdir(parents=True, exist_ok=True)


def _to_csv(data: list[dict], path: Path) -> None:
    if not data:
        path.write_text("", encoding="utf-8")
        return
    rows = []
    for d in data:
        flat = dict(d)
        if "resumen_flujos" in flat:
            flat["resumen_flujos"] = json.dumps(flat["resumen_flujos"], ensure_ascii=False)
        rows.append(flat)
    keys = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)


def exportar_resultados(
    procesos: list[dict],
    resultados: list[dict],
    comparaciones: list[dict],
    resumen: dict,
    expediente: str,
    salida: str | Path,
) -> dict[str, str]:
    out = Path(salida)
    _asegurar(out)

    rutas = {
        "procesos_json": out / "procesos_comparados.json",
        "procesos_csv": out / "procesos_comparados.csv",
        "resultados_json": out / "resultados_flujos.json",
        "resultados_csv": out / "resultados_flujos.csv",
        "comparaciones_json": out / "comparaciones_agente_proceso.json",
        "comparaciones_csv": out / "comparaciones_agente_proceso.csv",
        "resumen_json": out / "resumen_comparador.json",
        "expediente_md": out / "expediente_comparador_agente_proceso.md",
    }

    rutas["procesos_json"].write_text(json.dumps(procesos, ensure_ascii=False, indent=2), encoding="utf-8")
    rutas["resultados_json"].write_text(json.dumps(resultados, ensure_ascii=False, indent=2), encoding="utf-8")
    rutas["comparaciones_json"].write_text(json.dumps(comparaciones, ensure_ascii=False, indent=2), encoding="utf-8")
    rutas["resumen_json"].write_text(json.dumps(resumen, ensure_ascii=False, indent=2), encoding="utf-8")
    rutas["expediente_md"].write_text(expediente, encoding="utf-8")

    _to_csv(procesos, rutas["procesos_csv"])
    _to_csv(resultados, rutas["resultados_csv"])
    _to_csv(comparaciones, rutas["comparaciones_csv"])

    return {k: str(v) for k, v in rutas.items()}
