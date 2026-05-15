# 05 - Simulador Teams y Tareas IA

## Objetivo
Simular Teams, conversaciones, reuniones y tareas empresariales con IA simulada en entorno local.

## Estado actual
V1 local funcional mínima implementada.

## Entradas
- `datos_ejemplo/conversaciones_tareas_teams_sinteticas.json`
- `datos_ejemplo/configuracion_teams_tareas.json`

## Salidas
- Informe Markdown de actividad simulada.
- JSON de resultados por elemento.
- Registros individuales en `teams_simulado/`.

## Ejecución
`python .\proyectos\05-simulador-teams-tareas-ia\src\simulador_teams_tareas.py --items .\proyectos\05-simulador-teams-tareas-ia\datos_ejemplo\conversaciones_tareas_teams_sinteticas.json --config .\proyectos\05-simulador-teams-tareas-ia\datos_ejemplo\configuracion_teams_tareas.json --output-md .\proyectos\05-simulador-teams-tareas-ia\informes\informe_teams_tareas_ia.md --output-json .\proyectos\05-simulador-teams-tareas-ia\informes\resultado_teams_tareas_ia.json --teams-dir .\proyectos\05-simulador-teams-tareas-ia\teams_simulado`

## Límites
Sin Teams real, sin Planner real, sin To Do real, sin Microsoft Graph API real, sin OAuth real, sin Azure obligatorio y sin IA real.

##  Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  
(c) 2026 - Txema Ríos. Todos los derechos compartidos.

