# Decisiones Técnicas V1

## 1. Ejecución local sin cloud

Se prioriza ejecución local para eliminar dependencia de terceros, evitar costes variables y facilitar reproducibilidad en entorno de portfolio técnico.

## 2. Sin embeddings externos en V1

No se incorporan embeddings externos para mantener coste cero, simplicidad operativa y trazabilidad del comportamiento de recuperación sin cajas negras de proveedor.

## 3. Recuperación local simplificada

Se usa recuperación híbrida local (señal léxica + metadatos) como compromiso pragmático: suficiente para demostrar patrón RAG corporativo en V1 sin introducir infraestructura adicional (vector database real).

## 4. Generación extractiva en lugar de LLM externo

La respuesta se construye por extracción y composición local con citas obligatorias, reduciendo riesgo de alucinación y permitiendo auditar el origen de cada afirmación.

## 5. Valor de trazabilidad y citas

La trazabilidad por etapas y las citas explícitas permiten:
- auditar decisiones de recuperación,
- validar coherencia documental,
- justificar respuestas en revisión técnica,
- demostrar gobernanza básica en un flujo RAG corporativo.

## 6. Evaluación offline reproducible

Se mantiene un dataset dorado y una evaluación offline para medir consistencia sin depender de conectividad, APIs o disponibilidad de servicios externos.

## 7. Dependencias mínimas

Se usa `unittest` y utilidades estándar para reducir fricción de instalación y mantener el laboratorio portable.

## 🪪 Licencia y Autoría

Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.

© 2025 – Txema Ríos. Todos los derechos compartidos.
