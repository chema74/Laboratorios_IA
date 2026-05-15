# 07 - Gobierno de Permisos Microsoft Simulado

## Objetivo
Simular gobierno de permisos en entorno Microsoft empresarial ficticio aplicando mínimo privilegio.

## Estado actual
V1 local funcional mínima implementada.

## Entradas
- `datos_ejemplo/permisos_microsoft_simulados.json`
- `datos_ejemplo/configuracion_gobierno_permisos.json`

## Salidas
- Informe Markdown de decisiones de gobierno.
- JSON consolidado por permiso.
- Registros individuales en `registros/`.

## Ejecución
`python .\proyectos\07-gobierno-permisos-microsoft-simulado\src\gobierno_permisos_microsoft.py --permissions .\proyectos\07-gobierno-permisos-microsoft-simulado\datos_ejemplo\permisos_microsoft_simulados.json --config .\proyectos\07-gobierno-permisos-microsoft-simulado\datos_ejemplo\configuracion_gobierno_permisos.json --output-md .\proyectos\07-gobierno-permisos-microsoft-simulado\informes\informe_gobierno_permisos_microsoft.md --output-json .\proyectos\07-gobierno-permisos-microsoft-simulado\informes\resultado_gobierno_permisos_microsoft.json --registry-dir .\proyectos\07-gobierno-permisos-microsoft-simulado\registros`

## Límites
Sin Microsoft real, sin Microsoft Graph API real, sin OAuth real, sin Azure obligatorio y sin IA real.

##  Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  
(c) 2026 - Txema Ríos. Todos los derechos compartidos.

