# Guía de revisión de evidencias V2 - Laboratorio privacidad datos IA

## 1. Objetivo

Esta guía permite revisar de forma rápida si la V2 (Version 2 - Versión 2) del laboratorio `laboratorio-privacidad-datos-ia` está correctamente preparada para portfolio.

## 2. Revisión inicial

Desde la raíz del repositorio debe comprobarse:

- Rama V2 activa.
- Árbol Git limpio antes y después de las pruebas.
- Tests correctos.
- Documentación V2 presente.
- Scripts V2 presentes.
- Salidas locales generadas en `salidas/`.
- `main` no modificado.
- Web pública no modificada.

## 3. Comandos recomendados

Ejecutar:

`python .\scripts\validar_v2.py --json`

Ejecutar:

`python .\scripts\generar_informe_ejecutivo_v2.py --json`

Ejecutar:

`python -m pytest -q`

## 4. Qué debe observarse

La validación debe indicar resultado correcto.

El informe ejecutivo debe crearse en:

`salidas/informe_ejecutivo_v2.md`

El informe de validación debe crearse en:

`salidas/validacion_v2.md`

## 5. Señales de fallo

Debe revisarse manualmente si aparece cualquiera de estas señales:

- Mojibake visible en caracteres corruptos.
- Documentación V2 ausente.
- Licencia ausente.
- Referencias a datos personales reales.
- Dependencias cloud obligatorias.
- Cambios inesperados en `main`.
- Cambios en `chema74.github.io`.

## 6. Resultado esperado

Resultado esperado:

PRIVACIDAD_DATOS_IA_V2: OK

DATOS_REALES: NO

SIN_DATOS_PERSONALES_REALES: SI

WEB_PUBLICA: NO_MODIFICADA

##  Licencia y Autoría

Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.

(c) 2026 - Txema Ríos. Todos los derechos compartidos.

