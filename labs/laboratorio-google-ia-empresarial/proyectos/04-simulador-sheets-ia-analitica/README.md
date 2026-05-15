# Proyecto 04: Simulador Sheets IA Analítica (V1 local funcional)

## Objetivo
Simular análisis empresarial tipo Sheets con datos sintéticos y reglas analíticas locales.

## Alcance V1
- carga de CSV y validación de columnas;
- cálculo de indicadores operativos y financieros simulados;
- distribuciones y señales analíticas simuladas;
- hoja enriquecida local;
- informe Markdown y salida JSON.

## Ejecución
```powershell
python .\proyectos\04-simulador-sheets-ia-analitica\src\simulador_sheets_ia.py --sheet .\proyectos\04-simulador-sheets-ia-analitica\datos_ejemplo\hoja_operativa_sintetica.csv --config .\proyectos\04-simulador-sheets-ia-analitica\datos_ejemplo\configuracion_sheets_analitica.json --output-md .\proyectos\04-simulador-sheets-ia-analitica\informes\informe_sheets_ia_analitica.md --output-json .\proyectos\04-simulador-sheets-ia-analitica\informes\resultado_sheets_ia_analitica.json --sheets-dir .\proyectos\04-simulador-sheets-ia-analitica\hojas_simuladas
```

## Pruebas
```powershell
python -m unittest discover .\proyectos\04-simulador-sheets-ia-analitica\tests -v
```

## Límites
Sin Sheets real, sin OAuth real, sin APIs externas y sin IA real.

##  Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  
(c) 2026 - Txema Ríos. Todos los derechos compartidos.

