# 04 - Clasificador de Datos Sensibles Sintéticos (V1 local funcional mínima)

## Objetivo
Clasificar sensibilidad de datos sintéticos para aplicar controles defensivos de minimización, enmascarado y revisión humana.

## Funcionalidad implementada en V1
- Carga de registros y configuración local.
- Validación estructural y límites de uso no real.
- Clasificación de sensibilidad por placeholders y reglas simples.
- Cálculo de severidad simulada.
- Recomendación de acción defensiva.
- Marcado de minimización, enmascarado y revisión humana.
- Generación de texto enmascarado simulado.
- Resúmenes por sensibilidad y por acción defensiva.
- Generación de informe Markdown y salida JSON.

## Ejecución
```powershell
python .\proyectos\04-clasificador-datos-sensibles-sinteticos\src\clasificador_datos_sensibles.py --data .\proyectos\04-clasificador-datos-sensibles-sinteticos\datos_ejemplo\datos_sensibles_sinteticos.json --config .\proyectos\04-clasificador-datos-sensibles-sinteticos\datos_ejemplo\configuracion_clasificador_sensibilidad.json --output-md .\proyectos\04-clasificador-datos-sensibles-sinteticos\informes\informe_clasificacion_sensibilidad.md --output-json .\proyectos\04-clasificador-datos-sensibles-sinteticos\informes\resultado_clasificacion_sensibilidad.json
```

## Separación V1 y V2
- V1 actual: ejecución 100% local con reglas defensivas sintéticas.
- V2 futura (no implementada): evaluación opcional con APIs gratuitas usando `.env`, con fallback local si no hay variables o conectividad.

## 🪪 Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  
© 2025 – Txema Ríos. Todos los derechos compartidos.
