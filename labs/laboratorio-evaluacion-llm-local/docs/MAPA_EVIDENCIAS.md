# Mapa de Evidencias

Mapa de trazabilidad entre capacidades declaradas y artefactos reales del repositorio.

## 1. Dataset dorado sintético

- Evidencia: `datos/dataset_dorado.json`
- Generación/actualización: `python scripts\sembrar_datos.py`

## 2. Respuestas sintéticas candidatas

- Evidencia: `datos/respuestas_sinteticas.json`
- Generación/actualización: `python scripts\sembrar_datos.py`

## 3. Versionado de prompts para regresión

- Evidencia: `datos/prompts_versionados.json`
- Generación/actualización: `python scripts\sembrar_datos.py`

## 4. Evaluación consolidada

- Evidencia principal: `evaluacion/resultados/informe_evaluacion_llm.md`
- Generación: `python scripts\ejecutar_evaluacion.py`

## 5. Demo operativa

- Evidencia: salida de `python scripts\ejecutar_demo.py`
- Relación: permite inspección rápida del flujo antes de la evaluación completa.

## 6. Calidad funcional

- Evidencia: suite `tests/`
- Ejecución: `python -m unittest discover tests -v`

## Alcance V1

No se incluyen evidencias de cloud, embeddings ni LLM externo porque no forman parte de la implementación actual.

## 🪪 Licencia y Autoría

Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.

© 2025 – Txema Ríos. Todos los derechos compartidos.
