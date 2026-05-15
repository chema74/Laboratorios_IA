# 08 - Trazabilidad de Automatizaciones Microsoft

## Objetivo
Registrar trazabilidad local de automatizaciones Microsoft simuladas con identificador y hash reproducible.

## Estado actual
V1 local funcional mínima implementada.

## Entradas
- `datos_ejemplo/automatizaciones_microsoft_simuladas.json`
- `datos_ejemplo/configuracion_trazabilidad_automatizaciones.json`

## Salidas
- Informe Markdown de trazabilidad.
- JSON consolidado por automatización.
- Registros individuales en `registros/`.

## Ejecución
`python .\proyectos\08-trazabilidad-automatizaciones-microsoft\src\trazabilidad_automatizaciones_microsoft.py --automations .\proyectos\08-trazabilidad-automatizaciones-microsoft\datos_ejemplo\automatizaciones_microsoft_simuladas.json --config .\proyectos\08-trazabilidad-automatizaciones-microsoft\datos_ejemplo\configuracion_trazabilidad_automatizaciones.json --output-md .\proyectos\08-trazabilidad-automatizaciones-microsoft\informes\informe_trazabilidad_automatizaciones_microsoft.md --output-json .\proyectos\08-trazabilidad-automatizaciones-microsoft\informes\resultado_trazabilidad_automatizaciones_microsoft.json --registry-dir .\proyectos\08-trazabilidad-automatizaciones-microsoft\registros`

## Límites
Sin Microsoft real, sin Microsoft Graph API real, sin OAuth real, sin Azure obligatorio y sin IA real.

##  Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  
(c) 2026 - Txema Ríos. Todos los derechos compartidos.

