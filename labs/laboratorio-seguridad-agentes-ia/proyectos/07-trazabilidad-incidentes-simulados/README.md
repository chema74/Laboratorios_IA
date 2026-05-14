# 07 - Trazabilidad de Incidentes Simulados (V1 local funcional mínima)

## Objetivo
Registrar y trazar incidentes defensivos simulados con evidencias sintéticas y controles asociados.

## Funcionalidad implementada en V1
- Carga y validación de incidentes y configuración.
- Generación de identificador de evidencia por incidente.
- Cálculo de hash simulado para integridad de registro.
- Generación de registro JSON por incidente.
- Resúmenes por tipo, severidad y estado.
- Detección de trazabilidad débil y controles insuficientes.
- Generación de informe Markdown y JSON consolidado.

## Ejecución
```powershell
python .\proyectos\07-trazabilidad-incidentes-simulados\src\trazabilidad_incidentes.py --incidents .\proyectos\07-trazabilidad-incidentes-simulados\datos_ejemplo\incidentes_seguridad_simulados.json --config .\proyectos\07-trazabilidad-incidentes-simulados\datos_ejemplo\configuracion_trazabilidad_incidentes.json --output-md .\proyectos\07-trazabilidad-incidentes-simulados\informes\informe_trazabilidad_incidentes.md --output-json .\proyectos\07-trazabilidad-incidentes-simulados\informes\resultado_trazabilidad_incidentes.json --registry-dir .\proyectos\07-trazabilidad-incidentes-simulados\registros
```

## Separación V1 y V2
- V1: trazabilidad local defensiva sin servicios externos.
- V2 futura (no implementada): APIs gratuitas opcionales con `.env` y fallback local.

## 🪪 Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  
© 2025 – Txema Ríos. Todos los derechos compartidos.
