# Mapa de Evidencias

Relación entre capacidades del laboratorio y artefactos reales generados.

## 1. Informe de privacidad

- Evidencia principal: `informes/informe_privacidad_datos_ia.md`
- Generación: `python scripts\generar_informe_privacidad.py`

## 2. Dataset con PII ficticia

- Evidencia: `datos/dataset_con_pii_sintetica.json`
- Generación/actualización: `python scripts\sembrar_datos.py`

## 3. Políticas de privacidad sintéticas

- Evidencia: `datos/politicas_privacidad_sinteticas.json`
- Generación/actualización: `python scripts\sembrar_datos.py`

## 4. Prompts con contexto sensible

- Evidencia: `datos/prompts_con_contexto_sensible.json`
- Generación/actualización: `python scripts\sembrar_datos.py`

## 5. Salidas IA sintéticas

- Evidencia: `datos/salidas_ia_sinteticas.json`
- Generación/actualización: `python scripts\sembrar_datos.py`

## 6. Registro de tratamiento sintético

- Evidencia: `datos/registro_tratamiento_sintetico.json`
- Generación/actualización: `python scripts\sembrar_datos.py`

## 7. Calidad funcional

- Evidencia: suite `tests/`
- Ejecución: `python -m unittest discover tests -v`

## Alcance V1

No se incluyen evidencias de certificación legal o cumplimiento RGPD definitivo porque no forman parte del alcance implementado.

##  Licencia y Autoría

Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.

(c) 2026 - Txema Ríos. Todos los derechos compartidos.

