# Guía de revisión de evidencias V2 — Laboratorio backend IA empresarial

## 1. Objetivo

Esta guía permite revisar la V2 (Version 2 – Versión 2) del laboratorio `laboratorio-backend-ia-empresarial` sin tocar `main` y sin modificar la web pública.

## 2. Revisión recomendada

Ejecutar desde la rama V2:

`python .\scripts\validar_v2.py --json`

`python .\scripts\generar_informe_ejecutivo_v2.py --json`

`python -m pytest -q`

## 3. Qué debe comprobarse

La revisión debe confirmar:

- Existencia de documentación V2.
- Existencia de scripts V2.
- Existencia de tests V2.
- Licencia estándar en documentos Markdown.
- Ausencia de mojibake visible.
- Marcadores local-first y free-first.
- Ausencia de cloud obligatorio.
- Ausencia de APIs de pago obligatorias.
- Web pública no modificada.
- Sin merge a `main`.

## 4. Resultado esperado

El resultado esperado del validador es `OK`.

El resultado esperado de los tests es ejecución correcta.

El resultado esperado del informe ejecutivo es la creación de `salidas/informe_ejecutivo_v2.md`.

## 5. Interpretación

Si las validaciones pasan, el laboratorio queda preparado como V2 técnica documentada.

Si fallan, debe corregirse antes de crear tag de cierre.

## 6. Marcadores de control

LOCAL_FIRST: SI

FREE_FIRST: SI

WEB_PUBLICA: NO_MODIFICADA

MERGE_A_MAIN: NO_REALIZADO

## 🪪 Licencia y Autoría

Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.

© 2025 – Txema Ríos. Todos los derechos compartidos.
