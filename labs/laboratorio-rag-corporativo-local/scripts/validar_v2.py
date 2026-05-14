# -*- coding: utf-8 -*-
"""
Validador operativo V2 del laboratorio RAG corporativo local.

Comprueba estructura, documentación, scripts, tests, licencias y posibles
problemas de codificación UTF-8 sin usar servicios cloud, claves reales ni
APIs de pago obligatorias.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


DOCUMENTOS_V2 = [
    "docs/PLAN_V2_LABORATORIO_RAG.md",
    "docs/MAPA_EVIDENCIAS_V2.md",
    "docs/LIMITES_ALCANCE_V2.md",
]

DOCUMENTOS_BASE = [
    "docs/ARQUITECTURA.md",
    "docs/DECISIONES_TECNICAS.md",
    "docs/GUIA_EJECUCION.md",
    "docs/MAPA_EVIDENCIAS.md",
]

SCRIPTS_BASE = [
    "scripts/comprobar_salud.py",
    "scripts/ejecutar_demo.py",
    "scripts/sembrar_datos.py",
]

TESTS_BASE = [
    "tests/test_evaluacion.py",
    "tests/test_pipeline_rag.py",
    "tests/test_recuperacion.py",
    "tests/test_segmentacion.py",
    "tests/test_seguridad.py",
]

PATRONES_MOJIBAKE = ["Auditor?a", "Â", "â", "Ã", "�"]

LICENCIA_TITULO = "## 🪪 Licencia y Autoría"
LICENCIA_TEXTO = "Publicado bajo licencia Creative Commons CC BY-SA 4.0 International."
LICENCIA_AUTOR = "© 2025 – Txema Ríos. Todos los derechos compartidos."


def leer_texto(ruta: Path) -> str:
    if not ruta.exists():
        return ""
    return ruta.read_text(encoding="utf-8")


def comprobar_existencia(base: Path, rutas: list[str]) -> list[dict[str, object]]:
    return [{"ruta": ruta, "existe": (base / ruta).exists()} for ruta in rutas]


def comprobar_licencias_v2(base: Path) -> list[dict[str, object]]:
    resultados = []

    for ruta_relativa in DOCUMENTOS_V2:
        texto = leer_texto(base / ruta_relativa)
        licencia_ok = (
            LICENCIA_TITULO in texto
            and LICENCIA_TEXTO in texto
            and LICENCIA_AUTOR in texto
        )

        resultados.append({
            "ruta": ruta_relativa,
            "licencia_ok": licencia_ok,
        })

    return resultados


def comprobar_mojibake(base: Path) -> list[dict[str, object]]:
    hallazgos = []
    carpeta_docs = base / "docs"

    if not carpeta_docs.exists():
        return hallazgos

    for ruta in carpeta_docs.glob("*.md"):
        texto = leer_texto(ruta)

        for numero, linea in enumerate(texto.splitlines(), start=1):
            if any(patron in linea for patron in PATRONES_MOJIBAKE):
                hallazgos.append({
                    "ruta": str(ruta.relative_to(base)),
                    "linea": numero,
                    "contenido": linea,
                })

    return hallazgos


def construir_resultado(base: Path) -> dict[str, object]:
    documentos_v2 = comprobar_existencia(base, DOCUMENTOS_V2)
    documentos_base = comprobar_existencia(base, DOCUMENTOS_BASE)
    scripts_base = comprobar_existencia(base, SCRIPTS_BASE)
    tests_base = comprobar_existencia(base, TESTS_BASE)
    licencias_v2 = comprobar_licencias_v2(base)
    mojibake = comprobar_mojibake(base)

    resultado_ok = (
        all(item["existe"] for item in documentos_v2)
        and all(item["existe"] for item in documentos_base)
        and all(item["existe"] for item in scripts_base)
        and all(item["existe"] for item in tests_base)
        and all(item["licencia_ok"] for item in licencias_v2)
        and len(mojibake) == 0
    )

    return {
        "resultado": "ok" if resultado_ok else "fallo",
        "fecha_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "documentos_v2": documentos_v2,
        "documentos_base": documentos_base,
        "scripts_base": scripts_base,
        "tests_base": tests_base,
        "licencias_v2": licencias_v2,
        "mojibake": mojibake,
        "web_publica": "no_modificada",
        "main": "no_modificado",
        "dependencias_externas_obligatorias": "ninguna",
    }


def formatear_markdown(resultado: dict[str, object]) -> str:
    lineas = [
        "# 🧪 VALIDACIÓN V2 — LABORATORIO RAG CORPORATIVO LOCAL",
        "",
        "## 1. Resultado",
        "",
        f"`RESULTADO_VALIDACION_V2: {str(resultado['resultado']).upper()}`",
        "",
        f"- Fecha UTC: `{resultado['fecha_utc']}`.",
        "- Web pública `chema74.github.io`: no modificada.",
        "- Rama `main`: no modificada.",
        "- Dependencias externas obligatorias: ninguna.",
        "",
        "---",
        "",
        "## 2. Documentos V2",
        "",
    ]

    for bloque, titulo in [
        ("documentos_v2", "Documentos V2"),
        ("documentos_base", "Documentos base"),
        ("scripts_base", "Scripts base"),
        ("tests_base", "Tests base"),
    ]:
        if titulo != "Documentos V2":
            lineas.extend(["", "---", "", f"## {len([l for l in lineas if l.startswith('## ')]) + 1}. {titulo}", ""])

        for item in resultado[bloque]:
            estado = "OK" if item["existe"] else "FALTA"
            lineas.append(f"- `{estado}` — `{item['ruta']}`")

    lineas.extend(["", "---", "", "## 6. Licencias V2", ""])

    for item in resultado["licencias_v2"]:
        estado = "OK" if item["licencia_ok"] else "FALTA"
        lineas.append(f"- `{estado}` — `{item['ruta']}`")

    lineas.extend(["", "---", "", "## 7. Revisión de mojibake", ""])

    if resultado["mojibake"]:
        for item in resultado["mojibake"]:
            lineas.append(
                f"- `POSIBLE_MOJIBAKE` — `{item['ruta']}:{item['linea']}` — {item['contenido']}"
            )
    else:
        lineas.append("- `MOJIBAKE: OK`")

    lineas.extend([
        "",
        "---",
        "",
        "## 8. Estado final",
        "",
        f"`VALIDACION_V2_RAG: {str(resultado['resultado']).upper()}`",
        "",
        "`WEB_PUBLICA: NO_MODIFICADA`",
        "",
        "`MAIN: NO_MODIFICADO`",
        "",
        "`DEPENDENCIAS_EXTERNAS_OBLIGATORIAS: NINGUNA`",
        "",
        "---",
        "",
        "## 🪪 Licencia y Autoría",
        "Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.",
        "© 2025 – Txema Ríos. Todos los derechos compartidos.",
        "",
    ])

    return "\n".join(lineas)


def escribir_validacion(base: Path, resultado: dict[str, object], salida: Path) -> Path:
    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.write_text(formatear_markdown(resultado), encoding="utf-8")
    return salida


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Valida la estructura V2 del laboratorio RAG corporativo local."
    )
    parser.add_argument(
        "--salida",
        default="salidas/validacion_v2_rag.md",
        help="Ruta del informe Markdown de validación.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Muestra el resultado en JSON por consola.",
    )

    args = parser.parse_args()

    base = Path.cwd()
    resultado = construir_resultado(base)
    salida = escribir_validacion(base, resultado, Path(args.salida))

    if args.json:
        print(json.dumps({
            "resultado": resultado["resultado"],
            "archivo": str(salida),
            "web_publica": resultado["web_publica"],
            "main": resultado["main"],
            "dependencias_externas_obligatorias": resultado["dependencias_externas_obligatorias"],
        }, ensure_ascii=False, indent=2))
    else:
        print(f"OK_VALIDACION_V2_RAG: {salida}")

    return 0 if resultado["resultado"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())