# Catálogo V1

Catálogo de módulos del laboratorio de agentes enterprise y evidencia generada por cada bloque.

## Aplicación

- `app/main.py`: entrada CLI para ejecutar flujos de demo y escenario multiagente.
Evidencia: ejecución local controlada de escenarios.
- `app/config.py`: configuración de rutas y parámetros.
Evidencia: resolución coherente de datos e informes.
- `app/modelos.py`: estructuras de datos de tareas, acciones y resultados.
Evidencia: intercambio tipado entre agentes, orquestación y evaluación.

## Agentes

- `agentes/agente_planificador.py`: descomposición y planificación de tareas.
Evidencia: plan de acción usado por la orquestación.
- `agentes/agente_ejecutor.py`: ejecución de acciones simuladas vía herramientas.
Evidencia: resultados de ejecución por paso.
- `agentes/agente_revisor.py`: revisión de calidad/cumplimiento de resultados.
Evidencia: observaciones y validación posterior a ejecución.
- `agentes/agente_coordinador.py`: coordinación de ciclo multiagente.
Evidencia: secuencia completa de interacción entre roles.

## Herramientas simuladas

- `herramientas/crm_simulado.py`: operaciones sintéticas de CRM.
- `herramientas/calendario_simulado.py`: operaciones sintéticas de agenda.
- `herramientas/gestor_tickets_simulado.py`: gestión sintética de tickets.
- `herramientas/base_documental_simulada.py`: consulta sintética documental.
Evidencia: respuestas deterministas registradas en ejecución.

## Memoria y orquestación

- `memoria/memoria_operativa.py`: memoria temporal de estado del flujo.
- `memoria/registro_contexto.py`: registro de contexto operativo.
Evidencia: continuidad y trazabilidad de decisiones.
- `orquestacion/motor_orquestacion.py`: motor central de coordinación.
- `orquestacion/politicas_accion.py`: políticas aplicadas a acciones.
- `orquestacion/limites_accion.py`: límites operativos por agente/acción.
Evidencia: cumplimiento de reglas y control de alcance.

## Evaluación y observabilidad

- `evaluacion/evaluador_resultados.py`: evaluación de calidad de salida.
- `evaluacion/evaluador_trazabilidad.py`: evaluación de trazabilidad.
Evidencia: métricas de resultado en informes.
- `observabilidad/trazas.py`: trazas de ejecución.
- `observabilidad/costes_simulados.py`: coste simulado de operación.
Evidencia: auditoría de flujo y coste ficticio.

## Datos y salidas

- `datos/tareas_enterprise.json`: tareas sintéticas.
- `datos/herramientas_simuladas.json`: catálogo sintético de herramientas.
- `datos/politicas_agentes.json`: políticas y restricciones.
- `datos/escenarios_multiagente.json`: casos de coordinación multiagente.
- `informes/demo_agentes_enterprise.md`: evidencia de demo.
- `informes/escenario_multiagente.md`: evidencia de escenario multiagente.

## Scripts y pruebas

- `scripts/sembrar_datos.py`: preparación de datos sintéticos.
- `scripts/comprobar_salud.py`: chequeo de integridad operativa.
- `scripts/ejecutar_demo.py`: ejecución de demo base.
- `scripts/ejecutar_escenario_multiagente.py`: ejecución de escenario de coordinación.
- `tests/`: validación unitaria de agentes, límites, herramientas y evaluación.

##  Licencia y Autoría

Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.

(c) 2026 - Txema Ríos. Todos los derechos compartidos.

