# Decisiones Técnicas V1

## 1. Evaluación heurística y local

La evaluación se implementa con reglas heurísticas locales para garantizar reproducibilidad, bajo coste y capacidad de auditoría sin depender de terceros.

## 2. Sin modelos externos en V1

No se usan LLM externos para evitar variabilidad no controlada, costes por consumo y dependencia de disponibilidad de proveedores.

## 3. Uso de datasets dorados sintéticos

Se emplean datos sintéticos para:
- preservar privacidad,
- permitir distribución pública del repositorio,
- repetir experimentos de forma determinista.

## 4. Valor de rúbricas locales

Las rúbricas estructuran criterios de calidad comparables entre candidatas, facilitando revisión técnica y seguimiento de cambios.

## 5. Valor de la regresión de prompts

La regresión de prompts permite detectar degradaciones o mejoras entre versiones antes de adoptar cambios en flujos reales.

## 6. Límites frente a evaluación semántica avanzada

Este laboratorio no sustituye evaluaciones semánticas profundas ni juicio experto de dominio. Su función es aportar una capa inicial de control de calidad local y trazable.

## 7. Dependencias mínimas

Se prioriza librería estándar y `unittest` para simplificar instalación y mantener el laboratorio portable.

## 🪪 Licencia y Autoría

Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.

© 2025 – Txema Ríos. Todos los derechos compartidos.
