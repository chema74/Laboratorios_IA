# Arquitectura V1

Arquitectura local de agentes enterprise simulados con control de acciones, trazabilidad y evaluación reproducible.

## Flujo implementado

1. Tareas sintéticas
Carga de tareas y escenarios desde `datos/`.
2. Planificación
El agente planificador define secuencia de acciones.
3. Selección de herramientas
La orquestación asigna herramientas simuladas según tarea.
4. Ejecución simulada
El agente ejecutor opera sobre conectores sintéticos deterministas.
5. Memoria operativa
Persistencia temporal de contexto y resultados intermedios.
6. Revisión
El agente revisor valida consistencia y cobertura de resultado.
7. Coordinación
El agente coordinador gobierna transición entre etapas/roles.
8. Límites de acción
Aplicación de políticas y límites definidos en orquestación.
9. Evaluación
Evaluadores de resultados y trazabilidad.
10. Trazabilidad
Registro de trazas y coste simulado por ejecución.
11. Informes
Generación de `informes/demo_agentes_enterprise.md` y `informes/escenario_multiagente.md`.

## Componentes

- `agentes/`: roles funcionales del sistema multiagente.
- `herramientas/`: conectores simulados de dominio enterprise.
- `memoria/`: estado operativo y contexto.
- `orquestacion/`: coordinación, políticas y límites.
- `evaluacion/` y `observabilidad/`: calidad, trazas y costes simulados.

## Restricciones V1

- Sin LLM externo.
- Sin acciones reales sobre sistemas corporativos.
- Sin CRM/correo/calendario reales.
- Sin datos reales y sin automatización productiva.

## 🪪 Licencia y Autoría

Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.

© 2025 – Txema Ríos. Todos los derechos compartidos.
