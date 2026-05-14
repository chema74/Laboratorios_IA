# Mapa de evidencias V2 — Laboratorio privacidad datos IA

## 1. Finalidad

Este documento enumera las evidencias mínimas que permiten revisar la V2 (Version 2 – Versión 2) del laboratorio `laboratorio-privacidad-datos-ia`.

Las evidencias se centran en reproducibilidad local, trazabilidad documental y ausencia de dependencias obligatorias externas.

## 2. Evidencias documentales

La V2 incorpora los siguientes documentos:

- `docs/PLAN_V2_LABORATORIO_PRIVACIDAD_DATOS_IA.md`
- `docs/MAPA_EVIDENCIAS_V2.md`
- `docs/LIMITES_ALCANCE_V2.md`
- `docs/GUIA_REVISION_EVIDENCIAS_V2.md`

Estos documentos describen el alcance, los límites, la forma de revisión y el posicionamiento técnico del laboratorio.

## 3. Evidencias operativas

La V2 incorpora los siguientes scripts:

- `scripts/validar_v2.py`
- `scripts/generar_informe_ejecutivo_v2.py`

El primer script valida la presencia de documentación, marcadores de privacidad, ausencia de mojibake y licencia estándar.

El segundo script genera un informe ejecutivo local en `salidas/informe_ejecutivo_v2.md`.

## 4. Evidencias de test

La V2 incorpora los siguientes tests:

- `tests/test_validar_v2.py`
- `tests/test_generar_informe_ejecutivo_v2.py`

Estos tests comprueban que los scripts se ejecutan correctamente y generan salidas verificables.

## 5. Evidencias fuera de alcance

No se exige integración con servicios cloud.

No se exige conexión a APIs (Application Programming Interfaces – Interfaces de Programación de Aplicaciones) externas.

No se usan datos personales reales.

No se ofrece certificación normativa.

No se toca la web pública `chema74.github.io`.

## 6. Marcadores de control

DATOS_REALES: NO

SIN_DATOS_PERSONALES_REALES: SI

CLOUD_OBLIGATORIO: NO

API_PAGO_OBLIGATORIA: NO

WEB_PUBLICA: NO_MODIFICADA

## 🪪 Licencia y Autoría

Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.

© 2025 – Txema Ríos. Todos los derechos compartidos.
