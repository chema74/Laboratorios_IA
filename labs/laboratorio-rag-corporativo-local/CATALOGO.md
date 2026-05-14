# Catálogo de Componentes V1

Este catálogo describe qué parte del laboratorio hace cada módulo y qué evidencia observable deja para revisión técnica.

## Aplicación

- `app/main.py`: punto de entrada CLI para lanzar consultas y flujo principal.
Evidencia: ejecución interactiva y salida de respuesta con citas en demo.
- `app/config.py`: configuración de rutas y parámetros locales.
Evidencia: rutas consistentes usadas por scripts de salud y demo.
- `app/modelos.py`: estructuras de datos del dominio (dataclasses).
Evidencia: intercambio tipado entre segmentación, recuperación y generación.

## Núcleo RAG

- `componentes/segmentador.py`: segmentación del corpus en fragmentos trazables.
Evidencia: fragmentos referenciables por documento en las respuestas.
- `componentes/recuperador_hibrido.py`: recuperación híbrida local (léxico + metadatos).
Evidencia: ranking inicial de candidatos relevantes para cada consulta.
- `componentes/reordenador_resultados.py`: ajuste final de orden de resultados.
Evidencia: priorización final consumida por el generador extractivo.
- `servicios/pipeline_rag.py`: orquestación extremo a extremo del pipeline.
Evidencia: secuencia completa de etapas ejecutada en demo y evaluación.
- `servicios/generador_respuesta.py`: composición de respuesta extractiva con citas.
Evidencia: respuesta final con referencias explícitas a fuentes del corpus.

## Seguridad

- `seguridad/guardia_entrada.py`: validación básica de consultas de entrada.
Evidencia: rechazo/control de consultas no válidas según reglas locales.
- `seguridad/filtro_salida.py`: control de salida para exigir citas.
Evidencia: bloqueo o ajuste de salidas sin trazabilidad mínima.

## Observabilidad

- `observabilidad/trazas.py`: registro de eventos por etapa.
Evidencia: trazas de ejecución para auditoría técnica de la demo.
- `observabilidad/costes_simulados.py`: cálculo de coste ficticio por consulta.
Evidencia: coste estimado reportado sin uso de proveedores externos.

## Evaluación

- `evaluacion/dataset_dorado.json`: conjunto de consultas esperadas.
Evidencia: base estable para medición reproducible offline.
- `evaluacion/evaluacion_offline.py`: ejecución y resumen de métricas offline.
Evidencia: `evaluacion/resultados/resultado_evaluacion.md`.

## Scripts operativos

- `scripts/sembrar_datos.py`: generación/siembra de corpus sintético local.
Evidencia: `datos/brutos/documentos_corporativos.json`.
- `scripts/comprobar_salud.py`: verificación de estructura y dependencias mínimas.
Evidencia: salida de salud previa a demo/evaluación.
- `scripts/ejecutar_demo.py`: demo local con salida Markdown.
Evidencia: `evaluacion/resultados/demo_rag_corporativo.md`.

## Alcance V1

Este laboratorio demuestra un patrón RAG corporativo local reproducible con datos sintéticos y controles básicos de calidad. No incorpora cloud, LLM externos ni vector database real.

## 🪪 Licencia y Autoría

Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.

© 2025 – Txema Ríos. Todos los derechos compartidos.
