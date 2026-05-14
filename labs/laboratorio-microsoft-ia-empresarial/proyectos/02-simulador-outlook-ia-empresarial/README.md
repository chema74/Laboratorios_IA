# 02 - Simulador Outlook IA Empresarial

## Objetivo
Simular una bandeja Outlook empresarial con clasificacion, priorizacion y acciones sugeridas usando solo datos sinteticos.

## Estado actual
V1 local funcional minima implementada.

## Entradas
- `datos_ejemplo/correos_outlook_sinteticos.json`
- `datos_ejemplo/configuracion_outlook_simulado.json`

## Salidas
- Informe Markdown con distribuciones y recomendaciones.
- JSON de resultados por correo.
- Registros JSON individuales en `bandeja_simulada/`.

## Ejecucion
`python .\proyectos\02-simulador-outlook-ia-empresarial\src\simulador_outlook_ia.py --emails .\proyectos\02-simulador-outlook-ia-empresarial\datos_ejemplo\correos_outlook_sinteticos.json --config .\proyectos\02-simulador-outlook-ia-empresarial\datos_ejemplo\configuracion_outlook_simulado.json --output-md .\proyectos\02-simulador-outlook-ia-empresarial\informes\informe_outlook_ia_simulado.md --output-json .\proyectos\02-simulador-outlook-ia-empresarial\informes\resultado_outlook_ia_simulado.json --mailbox-dir .\proyectos\02-simulador-outlook-ia-empresarial\bandeja_simulada`

## Limites
Sin Outlook real, sin Microsoft Graph API real, sin OAuth real, sin Azure obligatorio y sin IA real.

## 🪪 Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  
© 2025 – Txema Ríos. Todos los derechos compartidos.
