# -*- coding: utf-8 -*-
"""Validador operativo V2 del laboratorio backend IA empresarial."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "docs/PLAN_V2_LABORATORIO_BACKEND_IA_EMPRESARIAL.md",
    "docs/MAPA_EVIDENCIAS_V2.md",
    "docs/LIMITES_ALCANCE_V2.md",
    "docs/GUIA_REVISION_EVIDENCIAS_V2.md",
    "scripts/validar_v2.py",
    "scripts/generar_informe_ejecutivo_v2.py",
    "tests/test_validar_v2.py",
    "tests/test_generar_informe_ejecutivo_v2.py",
]

LICENSE_SNIPPETS = [
    "Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.",
    "© 2025 – Txema Ríos. Todos los derechos compartidos.",
]

BAD_SEQUENCES = ["Â", "Ã", "â€“", "Auditor?a", "RÃ"]
REQUIRED_MARKERS = [
    "LOCAL_FIRST: SI",
    "FREE_FIRST: SI",
    "CLOUD_OBLIGATORIO: NO",
    "API_PAGO_OBLIGATORIA: NO",
    "WEB_PUBLICA: NO_MODIFICADA",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def validate() -> dict[str, object]:
    missing = [item for item in REQUIRED_FILES if not (REPO / item).exists()]
    markdown_files = [REPO / item for item in REQUIRED_FILES if item.endswith(".md") and (REPO / item).exists()]

    without_license = []
    mojibake = []
    marker_source = []

    for path in markdown_files:
        text = read_text(path)
        marker_source.append(text)
        if not all(snippet in text for snippet in LICENSE_SNIPPETS):
            without_license.append(str(path.relative_to(REPO)))
        if any(bad in text for bad in BAD_SEQUENCES):
            mojibake.append(str(path.relative_to(REPO)))

    combined = "\n".join(marker_source)
    missing_markers = [marker for marker in REQUIRED_MARKERS if marker not in combined]

    output_dir = REPO / "salidas"
    output_dir.mkdir(exist_ok=True)
    report = output_dir / "validacion_v2.md"
    status = "OK" if not missing and not without_license and not mojibake and not missing_markers else "ERROR"
    report.write_text(
        "# Validación V2 — Laboratorio backend IA empresarial\n\n"
        f"Resultado: {status}\n\n"
        "LOCAL_FIRST: SI\n\n"
        "FREE_FIRST: SI\n\n"
        "CLOUD_OBLIGATORIO: NO\n\n"
        "API_PAGO_OBLIGATORIA: NO\n\n"
        "WEB_PUBLICA: NO_MODIFICADA\n",
        encoding="utf-8",
    )

    ok = status == "OK"
    return {
        "resultado": "OK" if ok else "ERROR",
        "repositorio": "laboratorio-backend-ia-empresarial",
        "v2": "v2-laboratorio-backend-ia-empresarial",
        "archivos_requeridos": len(REQUIRED_FILES),
        "faltantes": missing,
        "sin_licencia": without_license,
        "mojibake": mojibake,
        "marcadores_ausentes": missing_markers,
        "local_first": "SI",
        "free_first": "SI",
        "cloud_obligatorio": "NO",
        "api_pago_obligatoria": "NO",
        "web_publica": "NO_MODIFICADA",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida la V2 del laboratorio backend IA empresarial.")
    parser.add_argument("--json", action="store_true", help="Muestra el resultado en JSON.")
    args = parser.parse_args()

    result = validate()
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Resultado: {result['resultado']}")

    return 0 if result["resultado"] == "OK" else 1


if __name__ == "__main__":
    raise SystemExit(main())
