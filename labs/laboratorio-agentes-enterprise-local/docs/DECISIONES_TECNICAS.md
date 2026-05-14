# Decisiones Técnicas V1

## 1. Agentes deterministas/simulados en V1

Se prioriza un comportamiento determinista para asegurar repetibilidad, facilitar depuración y permitir evaluación objetiva de flujos multiagente.

## 2. Sin LLM externo

No se usan LLM externos para eliminar variabilidad de proveedor, costes por uso y dependencia de conectividad.

## 3. Herramientas simuladas

Las herramientas (CRM, calendario, tickets, base documental) son simuladas para ensayar orquestación sin riesgo operativo sobre sistemas reales.

## 4. Valor de los límites de acción

Los límites de acción reducen riesgo de ejecución no deseada, refuerzan gobernanza y hacen auditable qué puede y no puede hacer cada agente.

## 5. Valor de trazabilidad y revisión

La trazabilidad de decisiones y la revisión explícita permiten:
- auditar el proceso multiagente,
- detectar fallos de coordinación,
- justificar resultados en revisión técnica.

## 6. Límites frente a sistemas agentic productivos

Este laboratorio no sustituye una plataforma agentic de producción con integración real, monitorización continua, controles de seguridad avanzados y supervisión humana operativa.

## 7. Enfoque local-first

Se usan dependencias mínimas y ejecución local para mantener coste cero y portabilidad en contexto de portfolio técnico.

## 🪪 Licencia y Autoría

Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.

© 2025 – Txema Ríos. Todos los derechos compartidos.
