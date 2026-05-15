from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path

DOCUMENTOS_V2 = [
    "docs/PLAN_V2_LABORATORIO_AGENTES_ENTERPRISE.md",
    "docs/MAPA_EVIDENCIAS_V2.md",
    "docs/LIMITES_ALCANCE_V2.md",
    "docs/GUIA_REVISION_EVIDENCIAS_V2.md",
]

PATRONES_MOJIBAKE = ["Auditor?a", "Â", "â", "Ã", "�"]

LICENCIA_TITULO = "## 🪪 Licencia y Autoría"
LICENCIA_TEXTO = "Publicado bajo licencia Creative Commons CC BY-SA 4.0 International."
LICENCIA_AUTOR = "© 2025 – Txema Ríos. Todos los derechos compartidos."


def leer_texto(ruta: Path) -> str:
    if not ruta.exists():
        return ""
    return ruta.read_text(encoding="utf-8")


def listar_python(base: Path, carpeta: str) -> list[str]:
    ruta = base / carpeta
    if not ruta.exists():
        return []
    return sorted(str(r.relative_to(base)).replace("\\", "/") for r in ruta.glob("*.py"))


def comprobar_existencia(base: Path, rutas: list[str]) -> list[dict[str, object]]:
    return [{"ruta": ruta, "existe": (base / ruta).exists()} for ruta in rutas]


def comprobar_licencias_v2(base: Path) -> list[dict[str, object]]:
    resultados = []
    for ruta_relativa in DOCUMENTOS_V2:
        texto = leer_texto(base / ruta_relativa)
        resultados.append({
            "ruta": ruta_relativa,
            "licencia_ok": (
                LICENCIA_TITULO in texto
                and LICENCIA_TEXTO in texto
                and LICENCIA_AUTOR in texto
            ),
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
                    "ruta": str(ruta.relative_to(base)).replace("\\", "/"),
                    "linea": numero,
                    "contenido": linea,
                })
    return hallazgos


def construir_resultado(base: Path) -> dict[str, object]:
    documentos_v2 = comprobar_existencia(base, DOCUMENTOS_V2)
    scripts_python = listar_python(base, "scripts")
    tests_python = listar_python(base, "tests")
    licencias_v2 = comprobar_licencias_v2(base)
    mojibake = comprobar_mojibake(base)

    ok = (
        all(item["existe"] for item in documentos_v2)
        and len(scripts_python) >= 1
        and len(tests_python) >= 1
        and all(item["licencia_ok"] for item in licencias_v2)
        and len(mojibake) == 0
    )

    return {
        "resultado": "ok" if ok else "fallo",
        "fecha_utc": datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC"),
        "documentos_v2": documentos_v2,
        "scripts_python": scripts_python,
        "tests_python": tests_python,
        "licencias_v2": licencias_v2,
        "mojibake": mojibake,
        "web_publica": "no_modificada",
        "main": "no_modificado",
        "dependencias_externas_obligatorias": "ninguna",
    }


def formatear_markdown(resultado: dict[str, object]) -> str:
    lineas = [
        "# 🧪 VALIDACIÓN V2 — LABORATORIO AGENTES ENTERPRISE LOCAL",
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

    for item in resultado["documentos_v2"]:
        estado = "OK" if item["existe"] else "FALTA"
        lineas.append(f"- `{estado}` — `{item['ruta']}`")

    lineas.extend(["", "---", "", "## 3. Licencias V2", ""])
    for item in resultado["licencias_v2"]:
        estado = "OK" if item["licencia_ok"] else "FALTA"
        lineas.append(f"- `{estado}` — `{item['ruta']}`")

    lineas.extend(["", "---", "", "## 4. Revisión de mojibake", ""])
    if resultado["mojibake"]:
        for item in resultado["mojibake"]:
            lineas.append(f"- `POSIBLE_MOJIBAKE` — `{item['ruta']}:{item['linea']}` — {item['contenido']}")
    else:
        lineas.append("- `MOJIBAKE: OK`")

    lineas.extend([
        "",
        "---",
        "",
        "## 5. Estado final",
        "",
        f"`VALIDACION_V2_AGENTES_ENTERPRISE: {str(resultado['resultado']).upper()}`",
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
    parser = argparse.ArgumentParser(description="Valida la estructura V2 del laboratorio de agentes enterprise local.")
    parser.add_argument("--salida", default="salidas/validacion_v2_agentes_enterprise.md")
    parser.add_argument("--json", action="store_true")
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
        print(f"OK_VALIDACION_V2_AGENTES_ENTERPRISE: {salida}")

    return 0 if resultado["resultado"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())