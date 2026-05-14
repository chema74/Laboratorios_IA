# 10 - Demo Completa de Seguridad de Agentes (V1 local funcional mínima)

## Objetivo
Construir una demo local integradora que recorra toda la cadena defensiva del laboratorio.

## Funcionalidad implementada en V1
- Carga escenario y configuración sintética.
- Genera guion de demo en Markdown.
- Genera expediente defensivo en Markdown.
- Genera mapa de controles defensivos en Markdown.
- Genera JSON consolidado de la demo.
- Referencia explícita de los 10 módulos del repositorio.

## Ejecución
```powershell
python .\proyectos\10-demo-seguridad-agentes-completa\src\demo_seguridad_agentes.py --scenario .\proyectos\10-demo-seguridad-agentes-completa\datos_ejemplo\escenario_seguridad_agentes.json --config .\proyectos\10-demo-seguridad-agentes-completa\datos_ejemplo\configuracion_demo_seguridad.json --output-dir .\proyectos\10-demo-seguridad-agentes-completa\demo
```

## Separación V1 y V2
- V1: demo local sintética sin servicios externos.
- V2 futura (no implementada): ampliación opcional con APIs gratuitas vía `.env` y fallback local.

## 🪪 Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  
© 2025 – Txema Ríos. Todos los derechos compartidos.
