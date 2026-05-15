# Decisiones Técnicas V1

## 1. Costes simulados en lugar de costes reales

Se usan costes simulados para mantener el laboratorio sin dependencias de proveedores, sin variación por tarifas externas y con resultados reproducibles.

## 2. Sin herramientas externas de observabilidad en V1

No se incorporan Prometheus, Grafana ni plataformas cloud para conservar instalación mínima y operación local inmediata en entorno de portfolio.

## 3. Panel HTML estático local

Se utiliza HTML estático para disponer de visualización simple, portable y auditable, sin backend adicional ni servicios de despliegue.

## 4. Valor de las métricas operativas

Medir latencia, degradación, errores, feedback y presupuesto permite:
- detectar riesgos tempranos,
- priorizar acciones de mejora,
- justificar decisiones técnicas con evidencia,
- ensayar gobernanza operativa básica de IA.

## 5. Límites frente a observabilidad productiva real

Este laboratorio no sustituye una plataforma de observabilidad productiva con telemetría distribuida, métricas de proveedor en tiempo real y alertado continuo.

## 6. Enfoque local-first y dependencias mínimas

Se prioriza librería estándar y `unittest` para minimizar fricción de uso y asegurar reproducibilidad en cualquier equipo local.

##  Licencia y Autoría

Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.

(c) 2026 - Txema Ríos. Todos los derechos compartidos.

