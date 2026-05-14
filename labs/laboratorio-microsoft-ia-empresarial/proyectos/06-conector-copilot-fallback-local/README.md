# 06 - Conector Copilot con Fallback Local

## Objetivo
Implementar un conector conceptual de Copilot que opera siempre en fallback local determinista.

## Estado actual
V1 local funcional mínima implementada.

## Entradas
- `datos_ejemplo/solicitudes_copilot_simuladas.json`
- `datos_ejemplo/configuracion_copilot_fallback.json`

## Salidas
- Informe Markdown de fallback.
- JSON consolidado por solicitud.
- Registros individuales en `respuestas_simuladas/`.

## Ejecución
`python .\proyectos\06-conector-copilot-fallback-local\src\conector_copilot_fallback.py --requests .\proyectos\06-conector-copilot-fallback-local\datos_ejemplo\solicitudes_copilot_simuladas.json --config .\proyectos\06-conector-copilot-fallback-local\datos_ejemplo\configuracion_copilot_fallback.json --output-md .\proyectos\06-conector-copilot-fallback-local\informes\informe_copilot_fallback_local.md --output-json .\proyectos\06-conector-copilot-fallback-local\informes\resultado_copilot_fallback_local.json --responses-dir .\proyectos\06-conector-copilot-fallback-local\respuestas_simuladas`

## Límites
Sin Copilot real, sin Microsoft Graph API real, sin OAuth real, sin Azure obligatorio, sin red y sin IA real.

## 🪪 Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  
© 2025 – Txema Ríos. Todos los derechos compartidos.
