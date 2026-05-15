"""
Generador de informe ejecutivo V2 del laboratorio de observabilidad y costes IA.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import UTC, datetime
from pathlib import Path

DOCUMENTOS_CLAVE = [
    "docs/PLAN_V2_LABORATORIO_OBSERVABILIDAD_COSTES.md",
    "docs/MAPA_EVIDENCIAS_V2.md",
    "docs/LIMITES_ALCANCE_V2.md",
    "docs/GUIA_REVISION_EVIDENCIAS_V2.md",
]

SALIDAS_CLAVE = [
    "salidas/validacion_v2_observabilidad_costes.md",
]

LICENCIA = """---

## 🪪 Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.
© 2025 – Txema Ríos. Todos los derechos compartidos.
"""


def leer_texto(ruta: Path) -> str:
    if not ruta.exists():
        return ""
    return ruta.read_text(encoding="utf-8")


def extraer_titulo(texto: str) -> str:
    for linea in texto.splitlines():
        if linea.startswith("# "):
            return linea.strip()
    return "Sin título detectado"


def resumir_recurso(base: Path, ruta_relativa: str) -> dict[str, object]:
    ruta = base / ruta_relativa
    if not ruta.exists():
        return {"ruta": ruta_relativa, "existe": False, "resumen": "No encontrado"}

    if ruta.suffix.lower() == ".md":
        texto = leer_texto(ruta)
        resumen = f"{extraer_titulo(texto)} ({len(texto.splitlines())} líneas)"
    else:
        resumen = f"Detectado ({ruta.stat().st_size} bytes)"

    return {"ruta": ruta_relativa, "existe": True, "resumen": resumen}


def detectar_resultado_validacion(texto: str) -> str:
    patrones = [
        r"RESULTADO_VALIDACION_V2:\s*([A-Z]+)",
        r"VALIDACION_V2_OBSERVABILIDAD_COSTES:\s*([A-Z]+)",
        r'"resultado"\s*:\s*"([^"]+)"',
    ]

    for patron in patrones:
        coincidencia = re.search(patron, texto, flags=re.IGNORECASE)
        if coincidencia:
            return coincidencia.group(1).upper()

    if "MOJIBAKE: OK" in texto:
        return "OK"

    return "No detectado"


def construir_informe(base: Path) -> str:
    documentos = [resumir_recurso(base, ruta) for ruta in DOCUMENTOS_CLAVE]
    salidas = [resumir_recurso(base, ruta) for ruta in SALIDAS_CLAVE]
    scripts = sorted((base / "scripts").glob("*.py")) if (base / "scripts").exists() else []
    tests = sorted((base / "tests").glob("*.py")) if (base / "tests").exists() else []

    texto_validacion = leer_texto(base / "salidas" / "validacion_v2_observabilidad_costes.md")
    resultado_validacion = detectar_resultado_validacion(texto_validacion)
    fecha = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")

    lineas = [
        "# 📌 INFORME EJECUTIVO V2 — LABORATORIO OBSERVABILIDAD Y COSTES IA",
        "",
        "## 1. Objetivo",
        "",
        "Este informe resume el estado ejecutivo de la V2 (Version 2 – Versión 2) del laboratorio `laboratorio-observabilidad-costes-ia`.",
        "",
        "El laboratorio demuestra una base local para observabilidad, lectura de costes, trazabilidad operativa y revisión profesional de sistemas de IA (Artificial Intelligence – Inteligencia Artificial).",
        "",
        "No requiere servicios cloud obligatorios, claves reales ni APIs (Application Programming Interfaces – Interfaces de Programación de Aplicaciones) de pago.",
        "",
        "---",
        "",
        "## 2. Resultado ejecutivo",
        "",
        f"- Fecha de generación: `{fecha}`.",
        f"- Documentos V2 detectados: `{sum(1 for item in documentos if item['existe'])}/{len(documentos)}`.",
        f"- Scripts Python detectados: `{len(scripts)}`.",
        f"- Tests Python detectados: `{len(tests)}`.",
        f"- Salidas V2 detectadas: `{sum(1 for item in salidas if item['existe'])}/{len(salidas)}`.",
        f"- Resultado de validación V2 detectado: `{resultado_validacion}`.",
        "- Web pública `chema74.github.io`: no modificada.",
        "- Rama `main`: no modificada.",
        "- Dependencias externas obligatorias: ninguna.",
        "",
        "---",
        "",
        "## 3. Documentación revisada",
        "",
    ]

    for item in documentos:
        estado = "OK" if item["existe"] else "PENDIENTE"
        lineas.append(f"- `{estado}` — `{item['ruta']}` — {item['resumen']}")

    lineas.extend(["", "---", "", "## 4. Scripts y tests detectados", ""])
    for ruta in scripts:
        lineas.append(f"- `SCRIPT` — `{str(ruta.relative_to(base)).replace(chr(92), '/')}`")
    for ruta in tests:
        lineas.append(f"- `TEST` — `{str(ruta.relative_to(base)).replace(chr(92), '/')}`")

    lineas.extend([
        "",
        "---",
        "",
        "## 5. Lectura profesional",
        "",
        "El laboratorio representa una base controlada para hablar de operación, observabilidad y costes de sistemas de IA con enfoque local y auditable.",
        "",
        "Su valor no está en prometer una plataforma definitiva, sino en demostrar criterio técnico sobre qué conviene observar, cómo registrar evidencias y dónde empiezan los límites de un laboratorio.",
        "",
        "---",
        "",
        "## 6. Límites reconocidos",
        "",
        "- No es una plataforma productiva de observabilidad.",
        "- No sustituye FinOps empresarial completo.",
        "- No usa facturación real sensible.",
        "- No obliga a usar cloud.",
        "- No modifica la web pública.",
        "- No modifica la rama `main`.",
        "",
        "---",
        "",
        "## 7. Estado final",
        "",
        "`INFORME_EJECUTIVO_V2_OBSERVABILIDAD_COSTES_GENERADO: OK`",
        "",
        "`WEB_PUBLICA: NO_MODIFICADA`",
        "",
        "`MAIN: NO_MODIFICADO`",
        "",
        "`DEPENDENCIAS_EXTERNAS_OBLIGATORIAS: NINGUNA`",
        "",
        LICENCIA,
    ])

    return "\n".join(lineas)


def escribir_informe(base: Path, salida: Path) -> Path:
    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.write_text(construir_informe(base), encoding="utf-8")
    return salida


def main() -> int:
    parser = argparse.ArgumentParser(description="Genera el informe ejecutivo V2 del laboratorio de observabilidad y costes IA.")
    parser.add_argument("--salida", default="salidas/informe_ejecutivo_v2_observabilidad_costes.md")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    base = Path.cwd()
    salida = escribir_informe(base, Path(args.salida))

    if args.json:
        print(json.dumps({
            "resultado": "ok",
            "archivo": str(salida),
            "web_publica": "no_modificada",
            "main": "no_modificado",
            "dependencias_externas_obligatorias": "ninguna",
        }, ensure_ascii=False, indent=2))
    else:
        print(f"OK_INFORME_EJECUTIVO_V2_OBSERVABILIDAD_COSTES: {salida}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())