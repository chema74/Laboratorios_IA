# Arquitectura V1

Arquitectura local orientada a evaluación heurística reproducible de respuestas generativas con datos sintéticos.

## Flujo implementado

1. Dataset dorado
Carga de `datos/dataset_dorado.json` como referencia de evaluación.
2. Respuestas sintéticas
Carga de candidatas desde `datos/respuestas_sinteticas.json`.
3. Rúbricas
Aplicación de criterios locales definidos en evaluadores.
4. Evaluación por criterios
Cálculo de consistencia, cobertura y señales de alucinación sintética.
5. Regresión de prompts
Comparación de desempeño entre variantes en `datos/prompts_versionados.json`.
6. Agregación de métricas
Síntesis de resultados por caso y métricas globales.
7. Generación de informe
Exportación de evidencia en `evaluacion/resultados/informe_evaluacion_llm.md`.
8. Observabilidad y costes simulados
Registro de trazas de ejecución y coste estimado local.

## Componentes

- `evaluadores/`: reglas y heurísticas de scoring.
- `servicios/`: orquestación y reporte final.
- `observabilidad/`: trazas y coste simulado.
- `scripts/`: ejecución operativa del flujo completo.

## Restricciones de diseño

- Sin LLM externo.
- Sin embeddings.
- Sin evaluación semántica profunda.
- Sin APIs externas y sin cloud.
- Sin datos reales.

Estas restricciones son deliberadas para mantener coste cero, control local y reproducibilidad documental en V1.

## 🪪 Licencia y Autoría

Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.

© 2025 – Txema Ríos. Todos los derechos compartidos.
