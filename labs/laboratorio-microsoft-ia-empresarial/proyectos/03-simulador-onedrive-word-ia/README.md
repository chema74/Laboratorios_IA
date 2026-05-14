# 03 - Simulador OneDrive y Word IA

## Objetivo
Simular flujos empresariales documentales de OneDrive y Word con acciones IA simuladas, sin integraciones reales.

## Estado actual
V1 local funcional mínima implementada.

## Entradas
- `datos_ejemplo/documentos_word_sinteticos.json`
- `datos_ejemplo/configuracion_onedrive_word_simulado.json`

## Salidas
- Informe Markdown de la simulación.
- JSON consolidado con resultados por documento.
- Registros JSON individuales en `documentos_simulados/`.

## Ejecución
`python .\proyectos\03-simulador-onedrive-word-ia\src\simulador_onedrive_word_ia.py --documents .\proyectos\03-simulador-onedrive-word-ia\datos_ejemplo\documentos_word_sinteticos.json --config .\proyectos\03-simulador-onedrive-word-ia\datos_ejemplo\configuracion_onedrive_word_simulado.json --output-md .\proyectos\03-simulador-onedrive-word-ia\informes\informe_onedrive_word_ia_simulado.md --output-json .\proyectos\03-simulador-onedrive-word-ia\informes\resultado_onedrive_word_ia_simulado.json --docs-dir .\proyectos\03-simulador-onedrive-word-ia\documentos_simulados`

## Límites
Sin OneDrive real, sin Word real, sin Microsoft Graph API real, sin OAuth real, sin Azure obligatorio y sin IA real.

## 🪪 Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  
© 2025 – Txema Ríos. Todos los derechos compartidos.
