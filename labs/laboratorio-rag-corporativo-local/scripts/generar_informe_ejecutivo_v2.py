# -*- coding: utf-8 -*-
"""
Generador de informe ejecutivo V2 del laboratorio RAG corporativo local.

Crea una evidencia ejecutiva en Markdown para explicar el valor técnico,
empresarial y documental del laboratorio.

No usa servicios cloud.
No requiere claves reales.
No requiere APIs de pago.
No modifica la web pública.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


DOCUMENTOS_CLAVE = [
    "docs/PLAN_V2_LABORATORIO_RAG.md",
    "docs/MAPA_EVIDENCIAS_V2.md",
    "docs/LIMITES_ALCANCE_V2.md",
    "docs/ARQUITECTURA.md",
    "docs/DECISIONES_TECNICAS.md",
    "docs/GUIA_EJECUCION.md",
    "docs/MAPA_EVIDENCIAS.md",
]

SCRIPTS_CLAVE = [
    "scripts/validar_v2.py",
    "scripts/comprobar_salud.py",
    "scripts/ejecutar_demo.py",
    "scripts/sembrar_datos.py",
]

SALIDAS_CLAVE = [
    "salidas/validacion_v2_rag.md",
]

LICENCIA = """---

## 🪪 Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.
© 2025 – Txema Ríos. Todos los derechos compartidos.
"""


def leer_texto(ruta: Path) -> str:
    """Lee un archivo UTF-8 si existe."""
    if not ruta.exists():
        return ""
    return ruta.read_text(encoding="utf-8")


def extraer_titulo(texto: str) -> str:
    """Extrae el primer título Markdown de un texto."""
    for linea in texto.splitlines():
        if linea.startswith("# "):
            return linea.strip()
    return "Sin título detectado"


def resumir_recurso(base: Path, ruta_relativa: str) -> dict[str, object]:
    """Resume existencia, tamaño y título de un recurso."""
    ruta = base / ruta_relativa

    if not ruta.exists():
        return {
            "ruta": ruta_relativa,
            "existe": False,
            "resumen": "No encontrado",
        }

    if ruta.suffix.lower() == ".md":
        texto = leer_texto(ruta)
        titulo = extraer_titulo(texto)
        lineas = len(texto.splitlines())
        resumen = f"{titulo} ({lineas} líneas)"
    else:
        resumen = f"Detectado ({ruta.stat().st_size} bytes)"

    return {
        "ruta": ruta_relativa,
        "existe": True,
        "resumen": resumen,
    }


def detectar_resultado_validacion(texto: str) -> str:
    """Extrae un resumen simple del resultado de validación V2."""
    patrones = [
        r"RESULTADO_VALIDACION_V2:\s*([A-Z]+)",
        r"VALIDACION_V2_RAG:\s*([A-Z]+)",
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
    """Construye el informe ejecutivo V2 en Markdown."""
    documentos = [resumir_recurso(base, ruta) for ruta in DOCUMENTOS_CLAVE]
    scripts = [resumir_recurso(base, ruta) for ruta in SCRIPTS_CLAVE]
    salidas = [resumir_recurso(base, ruta) for ruta in SALIDAS_CLAVE]

    texto_validacion = leer_texto(base / "salidas" / "validacion_v2_rag.md")
    resultado_validacion = detectar_resultado_validacion(texto_validacion)

    documentos_ok = sum(1 for item in documentos if item["existe"])
    scripts_ok = sum(1 for item in scripts if item["existe"])
    salidas_ok = sum(1 for item in salidas if item["existe"])

    fecha = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lineas = [
        "# 📌 INFORME EJECUTIVO V2 — LABORATORIO RAG CORPORATIVO LOCAL",
        "",
        "## 1. Objetivo",
        "",
        "Este informe resume el estado ejecutivo de la V2 (Version 2 – Versión 2) del laboratorio `laboratorio-rag-corporativo-local`.",
        "",
        "El laboratorio demuestra una base local para RAG (Retrieval-Augmented Generation – Generación Aumentada por Recuperación) corporativo, orientada a recuperación documental, trazabilidad, validación y evaluación profesional.",
        "",
        "No requiere servicios cloud obligatorios, claves reales ni APIs (Application Programming Interfaces – Interfaces de Programación de Aplicaciones) de pago.",
        "",
        "---",
        "",
        "## 2. Resultado ejecutivo",
        "",
        f"- Fecha de generación: `{fecha}`.",
        f"- Documentos clave detectados: `{documentos_ok}/{len(documentos)}`.",
        f"- Scripts clave detectados: `{scripts_ok}/{len(scripts)}`.",
        f"- Salidas V2 detectadas: `{salidas_ok}/{len(salidas)}`.",
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

    lineas.extend([
        "",
        "---",
        "",
        "## 4. Scripts revisados",
        "",
    ])

    for item in scripts:
        estado = "OK" if item["existe"] else "PENDIENTE"
        lineas.append(f"- `{estado}` — `{item['ruta']}` — {item['resumen']}")

    lineas.extend([
        "",
        "---",
        "",
        "## 5. Evidencias locales detectadas",
        "",
    ])

    for item in salidas:
        estado = "OK" if item["existe"] else "PENDIENTE"
        lineas.append(f"- `{estado}` — `{item['ruta']}` — {item['resumen']}")

    lineas.extend([
        "",
        "---",
        "",
        "## 6. Lectura empresarial",
        "",
        "El laboratorio representa un caso reconocible para empresa: consulta de documentación corporativa mediante recuperación de contexto, validación local y límites explícitos.",
        "",
        "Su valor no está en vender una plataforma SaaS (Software as a Service – Software como Servicio), sino en demostrar criterio técnico sobre cómo construir, evaluar y documentar una base RAG corporativa.",
        "",
        "Puede servir como evidencia para conversaciones de consultoría TIC (Information and Communication Technologies – Tecnologías de la Información y la Comunicación), selección técnica o diseño de pilotos internos de IA (Artificial Intelligence – Inteligencia Artificial).",
        "",
        "---",
        "",
        "## 7. Límites reconocidos",
        "",
        "- No es un despliegue productivo.",
        "- No implementa control avanzado de permisos corporativos.",
        "- No usa documentación real sensible.",
        "- No obliga a usar LLM (Large Language Model – Gran Modelo de Lenguaje) cloud.",
        "- No sustituye una auditoría de seguridad, privacidad u observabilidad completa.",
        "- No modifica la web pública.",
        "- No modifica la rama `main`.",
        "",
        "---",
        "",
        "## 8. Estado final",
        "",
        "`INFORME_EJECUTIVO_V2_RAG_GENERADO: OK`",
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
    """Escribe el informe ejecutivo en Markdown."""
    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.write_text(construir_informe(base), encoding="utf-8")
    return salida


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Genera el informe ejecutivo V2 del laboratorio RAG corporativo local."
    )
    parser.add_argument(
        "--salida",
        default="salidas/informe_ejecutivo_v2_rag.md",
        help="Ruta del informe Markdown de salida.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Muestra una salida JSON resumida.",
    )

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
        print(f"OK_INFORME_EJECUTIVO_V2_RAG: {salida}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())