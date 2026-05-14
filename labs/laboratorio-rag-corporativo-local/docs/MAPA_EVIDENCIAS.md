# Mapa de Evidencias

Este mapa vincula cada capacidad declarada en la V1 con artefactos reales del repositorio.

## 1. Ingesta documental sintética

- Evidencia: `datos/brutos/documentos_corporativos.json`
- Cómo se genera/actualiza: `python scripts\sembrar_datos.py`

## 2. Demo local de pipeline RAG

- Evidencia: `evaluacion/resultados/demo_rag_corporativo.md`
- Cómo se genera/actualiza: `python scripts\ejecutar_demo.py`

## 3. Evaluación offline

- Evidencia de entrada: `evaluacion/dataset_dorado.json`
- Evidencia de salida: `evaluacion/resultados/resultado_evaluacion.md`
- Cómo se genera/actualiza: `python evaluacion\evaluacion_offline.py`

## 4. Calidad funcional (tests)

- Evidencia: suite `tests/`
- Ejecución: `python -m unittest discover tests -v`

## 5. Salud operativa del entorno

- Evidencia: salida de verificación del script de salud
- Ejecución: `python scripts\comprobar_salud.py`

## Criterio de alcance

No se listan evidencias de cloud, embeddings externos, LLM externo ni vector database real porque esas capacidades no forman parte de la V1.

## 🪪 Licencia y Autoría

Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.

© 2025 – Txema Ríos. Todos los derechos compartidos.
