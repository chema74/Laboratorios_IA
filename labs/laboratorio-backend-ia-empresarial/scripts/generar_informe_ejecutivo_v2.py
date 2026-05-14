# -*- coding: utf-8 -*-
"""Generador de informe ejecutivo V2 del laboratorio backend IA empresarial."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def build_report() -> str:
    return """# Informe ejecutivo V2 — Laboratorio backend IA empresarial

## 1. Resumen

El laboratorio `laboratorio-backend-ia-empresarial` queda preparado como V2 técnica documentada para portfolio.

La V2 refuerza la capacidad de explicar una arquitectura backend con IA desde una perspectiva local-first, free-first, revisable y sin dependencias externas obligatorias.

## 2. Valor profesional

El repositorio demuestra criterios relevantes para una empresa:

- Separación entre arquitectura, validación y evidencias.
- Control de alcance.
- Ausencia de claves reales.
- Ausencia de servicios cloud obligatorios.
- Preparación para futuras integraciones mediante configuración externa.
- Generación de informes reproducibles.

## 3. Evidencias generadas

- `salidas/validacion_v2.md`
- `salidas/informe_ejecutivo_v2.md`

## 4. Marcadores

LOCAL_FIRST: SI

FREE_FIRST: SI

CLOUD_OBLIGATORIO: NO

API_PAGO_OBLIGATORIA: NO

WEB_PUBLICA: NO_MODIFICADA

MERGE_A_MAIN: NO_REALIZADO

## 🪪 Licencia y Autoría

Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.

© 2025 – Txema Ríos. Todos los derechos compartidos.
"""


def generate() -> dict[str, object]:
    output_dir = REPO / "salidas"
    output_dir.mkdir(exist_ok=True)
    path = output_dir / "informe_ejecutivo_v2.md"
    path.write_text(build_report(), encoding="utf-8")
    return {
        "resultado": "OK",
        "repositorio": "laboratorio-backend-ia-empresarial",
        "archivo": str(path.relative_to(REPO)),
        "local_first": "SI",
        "free_first": "SI",
        "web_publica": "NO_MODIFICADA",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Genera informe ejecutivo V2 del laboratorio backend IA empresarial.")
    parser.add_argument("--json", action="store_true", help="Muestra el resultado en JSON.")
    args = parser.parse_args()

    result = generate()
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Informe ejecutivo V2 generado: {result['archivo']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
