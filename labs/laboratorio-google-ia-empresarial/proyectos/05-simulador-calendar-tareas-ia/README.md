# Proyecto 05: Simulador Calendar y Tareas IA (V1 local funcional)

## Objetivo
Simular planificación de agenda y tareas empresariales sin Calendar real ni APIs reales.

## Alcance V1
- carga y validación de eventos/tareas sintéticos;
- detección de recordatorios y replanificación;
- cálculo de riesgo de retraso simulado;
- generación de agenda local y registros por elemento;
- informe Markdown y salida JSON.

## Ejecución
```powershell
python .\proyectos\05-simulador-calendar-tareas-ia\src\simulador_calendar_tareas.py --events .\proyectos\05-simulador-calendar-tareas-ia\datos_ejemplo\eventos_tareas_sinteticos.json --config .\proyectos\05-simulador-calendar-tareas-ia\datos_ejemplo\configuracion_calendar_tareas.json --output-md .\proyectos\05-simulador-calendar-tareas-ia\informes\informe_calendar_tareas_ia.md --output-json .\proyectos\05-simulador-calendar-tareas-ia\informes\resultado_calendar_tareas_ia.json --calendar-dir .\proyectos\05-simulador-calendar-tareas-ia\calendario_simulado
```

## Pruebas
```powershell
python -m unittest discover .\proyectos\05-simulador-calendar-tareas-ia\tests -v
```

## Límites
Sin Calendar real, sin OAuth real, sin Calendar API, sin cloud obligatorio y sin IA real.

##  Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  
(c) 2026 - Txema Ríos. Todos los derechos compartidos.

