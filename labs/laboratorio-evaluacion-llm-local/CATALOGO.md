# Catálogo V1

Catálogo de módulos del laboratorio y de la evidencia que aporta cada componente para revisión técnica.

## Aplicación

- `app/main.py`: entrada CLI para ejecutar evaluación local.
Evidencia: ejecución interactiva y flujo completo de evaluación.
- `app/config.py`: rutas y parámetros base del laboratorio.
Evidencia: configuración estable consumida por scripts y servicios.
- `app/modelos.py`: estructuras de datos de casos, respuestas y métricas.
Evidencia: intercambio coherente entre evaluadores y motor.

## Evaluadores

- `evaluadores/consistencia.py`: reglas de consistencia textual.
Evidencia: puntuaciones/cálculos de consistencia por caso.
- `evaluadores/cobertura.py`: verificación heurística de cobertura de criterios.
Evidencia: métricas de cobertura por respuesta candidata.
- `evaluadores/alucinaciones_sinteticas.py`: detección heurística de posibles alucinaciones sintéticas.
Evidencia: señales de riesgo incluidas en resultados de evaluación.
- `evaluadores/rubricas.py`: normalización y cálculo de rúbricas locales.
Evidencia: puntuación agregada por criterios.
- `evaluadores/regresion_prompts.py`: comparación entre versiones de prompt.
Evidencia: detección de regresión/mejora relativa entre variantes.
- `evaluadores/comparador_respuestas.py`: comparación de candidatas por caso.
Evidencia: priorización de respuesta con mejor desempeño heurístico.

## Servicios

- `servicios/motor_evaluacion.py`: orquestación de evaluación por criterios.
Evidencia: resultados consolidados por caso y métricas globales.
- `servicios/generador_informes.py`: emisión de informe Markdown final.
Evidencia: `evaluacion/resultados/informe_evaluacion_llm.md`.

## Observabilidad

- `observabilidad/trazas.py`: registro de eventos del pipeline evaluador.
Evidencia: trazabilidad de ejecución por etapa.
- `observabilidad/costes_simulados.py`: coste simulado del proceso.
Evidencia: estimación local de coste para análisis de operación.

## Datos

- `datos/dataset_dorado.json`: casos y expectativas sintéticas.
Evidencia: base de referencia reproducible para evaluación.
- `datos/respuestas_sinteticas.json`: respuestas candidatas de prueba.
Evidencia: insumo comparativo para métricas y rúbricas.
- `datos/prompts_versionados.json`: variantes de prompt para regresión.
Evidencia: histórico evaluable de cambios en prompts.

## Scripts y validación

- `scripts/sembrar_datos.py`: generación/actualización de datos sintéticos.
- `scripts/comprobar_salud.py`: chequeo operativo de estructura y módulos.
- `scripts/ejecutar_demo.py`: ejecución demostrativa del laboratorio.
- `scripts/ejecutar_evaluacion.py`: evaluación completa con informe.
- `tests/`: pruebas unitarias de evaluadores y motor.

##  Licencia y Autoría

Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.

(c) 2026 - Txema Ríos. Todos los derechos compartidos.

