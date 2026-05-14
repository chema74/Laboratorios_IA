# Arquitectura V1

Arquitectura local de observabilidad para sistemas IA simulados, orientada a evidencia reproducible y control operativo básico.

## Flujo implementado

1. Eventos sintéticos
Carga de `datos/eventos_ia_sinteticos.json` como base de operación.
2. Análisis de latencias
Cálculo de tiempos de respuesta y distribución temporal.
3. Cálculo de costes simulados
Estimación de coste ficticio por volumen y tipo de uso.
4. Presupuesto
Contraste contra `datos/presupuesto_operativo.json`.
5. Degradación
Detección de señales de empeoramiento de desempeño.
6. Feedback
Procesamiento de `datos/feedback_usuarios.json`.
7. Errores
Clasificación y recuento de incidencias en eventos.
8. Generación de informe
Salida en `informes/informe_observabilidad_costes_ia.md`.
9. Panel HTML local
Visualización estática en `panel/panel_observabilidad.html`.

## Componentes

- `observabilidad/`: análisis por dimensión operativa.
- `servicios/`: orquestación, simulación y reporte.
- `scripts/`: ejecución secuencial del flujo.
- `datos/`, `informes/`, `panel/`: entradas y evidencias resultantes.

## Restricciones V1

- Sin observabilidad cloud.
- Sin métricas de proveedor real.
- Sin Prometheus, Grafana ni servicios externos.
- Sin costes reales ni datos reales.

Estas restricciones mantienen el laboratorio en alcance local, educativo y de portfolio técnico.

## 🪪 Licencia y Autoría

Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.

© 2025 – Txema Ríos. Todos los derechos compartidos.
