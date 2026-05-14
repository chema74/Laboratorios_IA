# 05 - Control de Herramientas Simuladas (V1 local funcional mínima)

## Objetivo
Controlar el uso simulado de herramientas por agentes en entorno local defensivo.

## Funcionalidad implementada en V1
- Validación de solicitudes sintéticas.
- Evaluación de herramienta, acción y sensibilidad.
- Decisión defensiva: permitir, bloquear o revisar.
- Generación de registros JSON por solicitud.
- Resúmenes por herramienta y por decisión.
- Generación de informe Markdown y JSON consolidado.

## Ejecución
```powershell
python .\proyectos\05-control-herramientas-simuladas\src\control_herramientas_simuladas.py --requests .\proyectos\05-control-herramientas-simuladas\datos_ejemplo\solicitudes_herramientas_simuladas.json --config .\proyectos\05-control-herramientas-simuladas\datos_ejemplo\configuracion_control_herramientas.json --output-md .\proyectos\05-control-herramientas-simuladas\informes\informe_control_herramientas.md --output-json .\proyectos\05-control-herramientas-simuladas\informes\resultado_control_herramientas.json --registry-dir .\proyectos\05-control-herramientas-simuladas\registros
```

## Separación V1 y V2
- V1: simulación defensiva 100% local, sin herramientas reales ni red.
- V2 futura (no implementada): APIs gratuitas opcionales vía `.env` y fallback local.

## 🪪 Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  
© 2025 – Txema Ríos. Todos los derechos compartidos.
