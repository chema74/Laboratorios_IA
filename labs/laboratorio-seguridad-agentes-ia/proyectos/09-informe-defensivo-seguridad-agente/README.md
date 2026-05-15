# 09 - Informe Defensivo de Seguridad de Agente (V1 local funcional mínima)

## Objetivo
Generar un informe defensivo consolidado con métricas sintéticas de los módulos 01 a 08.

## Funcionalidad implementada en V1
- Carga resultados sintéticos agregados.
- Calcula puntuación global defensiva.
- Asigna nivel de madurez defensiva.
- Identifica riesgos principales y brechas de controles.
- Emite decisión defensiva recomendada.
- Genera informe Markdown y JSON consolidado.

## Ejecución
```powershell
python .\proyectos\09-informe-defensivo-seguridad-agente\src\generador_informe_defensivo.py --results .\proyectos\09-informe-defensivo-seguridad-agente\datos_ejemplo\resultados_seguridad_agente.json --config .\proyectos\09-informe-defensivo-seguridad-agente\datos_ejemplo\configuracion_informe_defensivo.json --output-md .\proyectos\09-informe-defensivo-seguridad-agente\informes\informe_defensivo_seguridad_agente.md --output-json .\proyectos\09-informe-defensivo-seguridad-agente\informes\informe_defensivo_seguridad_agente.json
```

## Separación V1 y V2
- V1: consolidación local con datos sintéticos.
- V2 futura (no implementada): integración opcional con APIs gratuitas vía `.env` y fallback local.

##  Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  
(c) 2026 - Txema Ríos. Todos los derechos compartidos.

