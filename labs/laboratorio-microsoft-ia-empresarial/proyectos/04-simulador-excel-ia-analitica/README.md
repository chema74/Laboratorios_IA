# 04 - Simulador Excel IA Analítica

## Objetivo
Simular análisis empresarial tipo Excel con métricas operativas y señales analíticas locales, sin integración real.

## Estado actual
V1 local funcional mínima implementada.

## Entradas
- `datos_ejemplo/libro_excel_operativo_sintetico.csv`
- `datos_ejemplo/configuracion_excel_analitica.json`

## Salidas
- Informe Markdown analítico.
- JSON con indicadores, distribuciones y señales simuladas.
- Libro enriquecido local en `libros_simulados/`.

## Ejecución
`python .\proyectos\04-simulador-excel-ia-analitica\src\simulador_excel_ia.py --workbook .\proyectos\04-simulador-excel-ia-analitica\datos_ejemplo\libro_excel_operativo_sintetico.csv --config .\proyectos\04-simulador-excel-ia-analitica\datos_ejemplo\configuracion_excel_analitica.json --output-md .\proyectos\04-simulador-excel-ia-analitica\informes\informe_excel_ia_analitica.md --output-json .\proyectos\04-simulador-excel-ia-analitica\informes\resultado_excel_ia_analitica.json --workbooks-dir .\proyectos\04-simulador-excel-ia-analitica\libros_simulados`

## Límites
Sin Excel real, sin Microsoft Graph API real, sin OAuth real, sin Azure obligatorio y sin IA real.

##  Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  
(c) 2026 - Txema Ríos. Todos los derechos compartidos.

