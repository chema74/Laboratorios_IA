# Mapa de evidencias V2 - Laboratorio backend IA empresarial

## 1. Finalidad

Este documento enumera las evidencias mínimas que permiten revisar la V2 (Version 2 - Versión 2) del laboratorio `laboratorio-backend-ia-empresarial`.

Las evidencias se centran en reproducibilidad local, claridad documental, ausencia de dependencias cloud obligatorias y trazabilidad de los resultados.

## 2. Evidencias documentales

La V2 incorpora los siguientes documentos:

- `docs/PLAN_V2_LABORATORIO_BACKEND_IA_EMPRESARIAL.md`
- `docs/MAPA_EVIDENCIAS_V2.md`
- `docs/LIMITES_ALCANCE_V2.md`
- `docs/GUIA_REVISION_EVIDENCIAS_V2.md`

Estos documentos describen alcance, límites, evidencias y forma de revisión.

## 3. Evidencias operativas

La V2 incorpora los siguientes scripts:

- `scripts/validar_v2.py`
- `scripts/generar_informe_ejecutivo_v2.py`

El primer script valida la estructura mínima, licencia, mojibake y marcadores de control.

El segundo script genera un informe ejecutivo local en `salidas/informe_ejecutivo_v2.md`.

## 4. Evidencias de test

La V2 incorpora los siguientes tests:

- `tests/test_validar_v2.py`
- `tests/test_generar_informe_ejecutivo_v2.py`

Estos tests comprueban que los scripts se ejecutan correctamente y generan salidas verificables.

## 5. Evidencias fuera de alcance

No se exige despliegue cloud.

No se exige conexión a APIs externas.

No se exige uso de claves reales.

No se modifica la web pública `chema74.github.io`.

## 6. Marcadores de control

LOCAL_FIRST: SI

FREE_FIRST: SI

CLOUD_OBLIGATORIO: NO

API_PAGO_OBLIGATORIA: NO

WEB_PUBLICA: NO_MODIFICADA

##  Licencia y Autoría

Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.

(c) 2026 - Txema Ríos. Todos los derechos compartidos.

