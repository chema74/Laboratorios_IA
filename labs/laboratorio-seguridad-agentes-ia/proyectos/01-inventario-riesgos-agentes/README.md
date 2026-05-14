# 01 - Inventario de Riesgos de Agentes (V1 local funcional mínima)

## Objetivo
Inventariar riesgos defensivos sintéticos de agentes de IA para priorizar controles y trazabilidad en entorno local, sin IA real ni servicios externos.

## Funcionalidad implementada en V1
- Carga y validación de riesgos sintéticos desde JSON.
- Validación de categorías, severidad, estado de control y banderas de alcance.
- Cálculo de puntuación de riesgo simulada y asignación de nivel (`bajo`, `medio`, `alto`, `critico`).
- Resúmenes por categoría y severidad.
- Detección de riesgos críticos, baja detectabilidad y controles insuficientes.
- Generación de informe Markdown y JSON validado.

## Ejecución
```powershell
python .\proyectos\01-inventario-riesgos-agentes\src\inventario_riesgos.py --risks .\proyectos\01-inventario-riesgos-agentes\datos_ejemplo\riesgos_agentes_sinteticos.json --config .\proyectos\01-inventario-riesgos-agentes\datos_ejemplo\configuracion_inventario_riesgos.json --output-md .\proyectos\01-inventario-riesgos-agentes\informes\informe_inventario_riesgos.md --output-json .\proyectos\01-inventario-riesgos-agentes\informes\inventario_riesgos_validado.json
```

## 🪪 Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  
© 2025 – Txema Ríos. Todos los derechos compartidos.
