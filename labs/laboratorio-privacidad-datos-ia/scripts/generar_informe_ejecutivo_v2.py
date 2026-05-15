"""
Generador de informe ejecutivo V2 para laboratorio-privacidad-datos-ia.

El informe resume el valor del laboratorio para portfolio, sus límites y sus
evidencias locales. No procesa datos reales y no usa servicios externos.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def construir_informe() -> str:
    return """# Informe ejecutivo V2 — Laboratorio privacidad datos IA

## 1. Resumen

El laboratorio `laboratorio-privacidad-datos-ia` queda preparado como evidencia técnica de privacidad aplicada a IA (Artificial Intelligence – Inteligencia Artificial) desde un enfoque local-first y free-first.

La V2 (Version 2 – Versión 2) no pretende certificar cumplimiento legal. Su valor está en mostrar trazabilidad, límites de alcance, ausencia de datos personales reales y evidencias reproducibles.

## 2. Valor profesional

El laboratorio permite explicar a una PYME (Small and Medium-sized Enterprise – Pequeña y Mediana Empresa) cómo revisar un sistema de IA desde criterios mínimos de privacidad:

- Separación entre datos reales y datos sintéticos.
- Control de dependencias externas.
- Documentación de límites.
- Validación local.
- Generación de evidencias.
- Advertencia expresa de no asesoría legal.

## 3. Relación con privacidad y gobernanza

El laboratorio menciona RGPD (General Data Protection Regulation – Reglamento General de Protección de Datos), DPIA (Data Protection Impact Assessment – Evaluación de Impacto relativa a la Protección de Datos) y AI Act (Artificial Intelligence Act – Reglamento de Inteligencia Artificial) como contexto técnico.

No sustituye revisión jurídica.

## 4. Evidencias generadas

Evidencias esperadas:

- `salidas/validacion_v2.md`
- `salidas/informe_ejecutivo_v2.md`

## 5. Marcadores de control

DATOS_REALES: NO

SIN_DATOS_PERSONALES_REALES: SI

ASESORIA_LEGAL: NO

CLOUD_OBLIGATORIO: NO

API_PAGO_OBLIGATORIA: NO

WEB_PUBLICA: NO_MODIFICADA

MERGE_A_MAIN: NO_REALIZADO

## 🪪 Licencia y Autoría

Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.

© 2025 – Txema Ríos. Todos los derechos compartidos.
"""


def generar() -> dict[str, object]:
    salida = REPO / "salidas"
    salida.mkdir(exist_ok=True)

    ruta = salida / "informe_ejecutivo_v2.md"
    ruta.write_text(construir_informe(), encoding="utf-8")

    return {
        "resultado": "OK",
        "repositorio": "laboratorio-privacidad-datos-ia",
        "archivo": str(ruta.relative_to(REPO)),
        "datos_reales": "NO",
        "sin_datos_personales_reales": "SI",
        "web_publica": "NO_MODIFICADA",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Genera informe ejecutivo V2 del laboratorio de privacidad.")
    parser.add_argument("--json", action="store_true", help="Muestra el resultado en JSON.")
    args = parser.parse_args()

    resultado = generar()

    if args.json:
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
    else:
        print(f"Informe ejecutivo V2 generado: {resultado['archivo']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
