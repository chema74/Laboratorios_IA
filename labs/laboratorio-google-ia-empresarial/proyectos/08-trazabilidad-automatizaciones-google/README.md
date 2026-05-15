# Proyecto 08: Trazabilidad de Automatizaciones Google (V1 local funcional)

## Objetivo
Registrar trazabilidad local de automatizaciones Google simuladas con evidencias y revisión controlada.

## Alcance V1
- carga y validación de automatizaciones sintéticas;
- generación de `id_traza` y hash simulado;
- evaluación de suficiencia de trazabilidad;
- detección de revisión requerida;
- generación de evidencia y registro local por automatización;
- informe Markdown y salida JSON.

## Ejecución
```powershell
python .\proyectos\08-trazabilidad-automatizaciones-google\src\trazabilidad_automatizaciones_google.py --automations .\proyectos\08-trazabilidad-automatizaciones-google\datos_ejemplo\automatizaciones_google_simuladas.json --config .\proyectos\08-trazabilidad-automatizaciones-google\datos_ejemplo\configuracion_trazabilidad_automatizaciones.json --output-md .\proyectos\08-trazabilidad-automatizaciones-google\informes\informe_trazabilidad_automatizaciones_google.md --output-json .\proyectos\08-trazabilidad-automatizaciones-google\informes\resultado_trazabilidad_automatizaciones_google.json --registry-dir .\proyectos\08-trazabilidad-automatizaciones-google\registros
```

## Pruebas
```powershell
python -m unittest discover .\proyectos\08-trazabilidad-automatizaciones-google\tests -v
```

## Límites
Sin Google real, sin OAuth real, sin APIs externas, sin cloud y sin IA real.

##  Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  
(c) 2026 - Txema Ríos. Todos los derechos compartidos.

