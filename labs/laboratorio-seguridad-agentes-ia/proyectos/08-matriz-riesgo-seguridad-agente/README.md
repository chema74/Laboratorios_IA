# 08 - Matriz de Riesgo de Seguridad del Agente (V1 local funcional mínima)

## Objetivo
Construir una matriz local de riesgo de seguridad para agentes con escenarios sintéticos, severidad y controles defensivos.

## Funcionalidad implementada en V1
- Carga y validación de escenarios y configuración.
- Cálculo de puntuación de riesgo por impactos y probabilidad.
- Asignación de nivel de riesgo (`bajo`, `medio`, `alto`, `critico`).
- Generación de matriz probabilidad x impacto.
- Resúmenes por nivel, categoría y activo simulado.
- Detección de riesgos críticos, baja detectabilidad y controles insuficientes.
- Generación de informe Markdown y JSON consolidado.

## Ejecución
```powershell
python .\proyectos\08-matriz-riesgo-seguridad-agente\src\matriz_riesgo_seguridad.py --scenarios .\proyectos\08-matriz-riesgo-seguridad-agente\datos_ejemplo\escenarios_riesgo_seguridad.json --config .\proyectos\08-matriz-riesgo-seguridad-agente\datos_ejemplo\configuracion_matriz_seguridad.json --output-md .\proyectos\08-matriz-riesgo-seguridad-agente\informes\informe_matriz_riesgo_seguridad.md --output-json .\proyectos\08-matriz-riesgo-seguridad-agente\informes\resultado_matriz_riesgo_seguridad.json
```

## Separación V1 y V2
- V1: matriz local defensiva con datos sintéticos.
- V2 futura (no implementada): evaluación opcional con APIs gratuitas vía `.env` y fallback local.

##  Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  
(c) 2026 - Txema Ríos. Todos los derechos compartidos.

