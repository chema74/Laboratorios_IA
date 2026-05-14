# 03 - Detector de Entradas de Riesgo (V1 local funcional mínima)

## Objetivo
Detectar entradas sintéticas de riesgo en interacciones simuladas para activar políticas defensivas, bloqueo y revisión humana cuando corresponda.

## Funcionalidad implementada en V1
- Carga de entradas y configuración defensiva local.
- Validación estructural y de límites (`usa_* = false`).
- Detección de categoría de riesgo por reglas simples y patrones sintéticos.
- Asignación de severidad simulada y política activada.
- Marcado de bloqueo y revisión humana.
- Resúmenes por categoría y severidad.
- Generación de informe Markdown y salida JSON.

## Ejecución
```powershell
python .\proyectos\03-detector-entradas-riesgo\src\detector_entradas_riesgo.py --inputs .\proyectos\03-detector-entradas-riesgo\datos_ejemplo\entradas_riesgo_sinteticas.json --config .\proyectos\03-detector-entradas-riesgo\datos_ejemplo\configuracion_detector_riesgo.json --output-md .\proyectos\03-detector-entradas-riesgo\informes\informe_detector_entradas_riesgo.md --output-json .\proyectos\03-detector-entradas-riesgo\informes\resultado_detector_entradas_riesgo.json
```

## Separación V1 y V2
- V1 actual: local-first, sin APIs externas, sin cloud, sin IA real.
- V2 futura (no implementada): integración opcional con APIs gratuitas controladas por `.env`, manteniendo fallback local obligatorio.

## 🪪 Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  
© 2025 – Txema Ríos. Todos los derechos compartidos.
