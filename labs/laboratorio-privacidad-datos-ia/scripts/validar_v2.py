# -*- coding: utf-8 -*-
"""
Validador operativo V2 para laboratorio-privacidad-datos-ia.

1. Comprueba que la documentación V2 esperada existe.
2. Comprueba que los scripts y tests V2 esperados existen.
3. Revisa licencia estándar en documentos Markdown.
4. Detecta señales básicas de mojibake.
5. Genera una evidencia local en salidas/validacion_v2.md.

No usa datos reales, no llama a servicios cloud y no requiere APIs externas.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List


REPO = Path(__file__).resolve().parents[1]

ARCHIVOS_REQUERIDOS = [
    "docs/PLAN_V2_LABORATORIO_PRIVACIDAD_DATOS_IA.md",
    "docs/MAPA_EVIDENCIAS_V2.md",
    "docs/LIMITES_ALCANCE_V2.md",
    "docs/GUIA_REVISION_EVIDENCIAS_V2.md",
    "scripts/validar_v2.py",
    "scripts/generar_informe_ejecutivo_v2.py",
    "tests/test_validar_v2.py",
    "tests/test_generar_informe_ejecutivo_v2.py",
]

DOCUMENTOS_CON_LICENCIA = [
    "docs/PLAN_V2_LABORATORIO_PRIVACIDAD_DATOS_IA.md",
    "docs/MAPA_EVIDENCIAS_V2.md",
    "docs/LIMITES_ALCANCE_V2.md",
    "docs/GUIA_REVISION_EVIDENCIAS_V2.md",
]

MARCADORES_REQUERIDOS = [
    "SIN_DATOS_PERSONALES_REALES: SI",
    "DATOS_REALES: NO",
    "CLOUD_OBLIGATORIO: NO",
    "API_PAGO_OBLIGATORIA: NO",
    "WEB_PUBLICA: NO_MODIFICADA",
]

PATRONES_MOJIBAKE = ["Â©", "â€“", "RÃ", "Auditor?a", "Privacidad?"]


def leer_texto_relativo(ruta_relativa: str) -> str:
    return (REPO / ruta_relativa).read_text(encoding="utf-8")


def validar_repositorio() -> Dict[str, object]:
    faltantes: List[str] = []
    sin_licencia: List[str] = []
    mojibake: List[str] = []
    marcadores_ausentes: List[str] = []

    for ruta in ARCHIVOS_REQUERIDOS:
        if not (REPO / ruta).exists():
            faltantes.append(ruta)

    for ruta in DOCUMENTOS_CON_LICENCIA:
        archivo = REPO / ruta
        if not archivo.exists():
            continue

        texto = archivo.read_text(encoding="utf-8")

        if "Creative Commons CC BY-SA 4.0 International" not in texto:
            sin_licencia.append(ruta)

        if "© 2025 – Txema Ríos. Todos los derechos compartidos." not in texto:
            sin_licencia.append(ruta)

        if any(patron in texto for patron in PATRONES_MOJIBAKE):
            mojibake.append(ruta)

    textos_docs = "\n".join(
        leer_texto_relativo(ruta)
        for ruta in DOCUMENTOS_CON_LICENCIA
        if (REPO / ruta).exists()
    )

    for marcador in MARCADORES_REQUERIDOS:
        if marcador not in textos_docs:
            marcadores_ausentes.append(marcador)

    correcto = not faltantes and not sin_licencia and not mojibake and not marcadores_ausentes

    return {
        "resultado": "OK" if correcto else "ERROR",
        "repositorio": "laboratorio-privacidad-datos-ia",
        "v2": "v2-laboratorio-privacidad-datos-ia",
        "archivos_requeridos": len(ARCHIVOS_REQUERIDOS),
        "faltantes": faltantes,
        "sin_licencia": sorted(set(sin_licencia)),
        "mojibake": mojibake,
        "marcadores_ausentes": marcadores_ausentes,
        "datos_reales": "NO",
        "sin_datos_personales_reales": "SI",
        "cloud_obligatorio": "NO",
        "api_pago_obligatoria": "NO",
        "web_publica": "NO_MODIFICADA",
    }


def generar_markdown(resultado: Dict[str, object]) -> str:
    estado = resultado["resultado"]

    lineas = [
        "# Validación V2 — Laboratorio privacidad datos IA",
        "",
        f"Resultado: {estado}",
        "",
        "Repositorio: laboratorio-privacidad-datos-ia",
        "",
        "Rama esperada: v2-laboratorio-privacidad-datos-ia",
        "",
        "## Controles",
        "",
        f"Archivos requeridos: {resultado['archivos_requeridos']}",
        f"Faltantes: {len(resultado['faltantes'])}",
        f"Documentos sin licencia: {len(resultado['sin_licencia'])}",
        f"Documentos con mojibake: {len(resultado['mojibake'])}",
        f"Marcadores ausentes: {len(resultado['marcadores_ausentes'])}",
        "",
        "## Marcadores de privacidad",
        "",
        "DATOS_REALES: NO",
        "SIN_DATOS_PERSONALES_REALES: SI",
        "CLOUD_OBLIGATORIO: NO",
        "API_PAGO_OBLIGATORIA: NO",
        "WEB_PUBLICA: NO_MODIFICADA",
        "",
        "## 🪪 Licencia y Autoría",
        "",
        "Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.",
        "",
        "© 2025 – Txema Ríos. Todos los derechos compartidos.",
    ]

    return "\n".join(lineas) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida la V2 del laboratorio de privacidad de datos IA.")
    parser.add_argument("--json", action="store_true", help="Muestra el resultado en JSON.")
    args = parser.parse_args()

    resultado = validar_repositorio()

    salida = REPO / "salidas"
    salida.mkdir(exist_ok=True)
    (salida / "validacion_v2.md").write_text(generar_markdown(resultado), encoding="utf-8")

    if args.json:
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
    else:
        print(f"Resultado final V2: {resultado['resultado']}")

    return 0 if resultado["resultado"] == "OK" else 1


if __name__ == "__main__":
    raise SystemExit(main())
