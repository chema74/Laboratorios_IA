# Proyecto 03: Simulador Drive/Docs IA (V1 local funcional)

## Objetivo
Simular flujos empresariales de gestión documental inspirados en Drive/Docs sin usar servicios reales.

## Alcance V1
- carga y validación de documentos sintéticos;
- resumen, etiquetado y sensibilidad simulados;
- detección de revisión humana;
- registro local por documento;
- informe Markdown y salida JSON.

## Ejecución
```powershell
python .\proyectos\03-simulador-drive-docs-ia\src\simulador_drive_docs_ia.py --documents .\proyectos\03-simulador-drive-docs-ia\datos_ejemplo\documentos_empresariales_sinteticos.json --config .\proyectos\03-simulador-drive-docs-ia\datos_ejemplo\configuracion_drive_docs_simulado.json --output-md .\proyectos\03-simulador-drive-docs-ia\informes\informe_drive_docs_ia_simulado.md --output-json .\proyectos\03-simulador-drive-docs-ia\informes\resultado_drive_docs_ia_simulado.json --docs-dir .\proyectos\03-simulador-drive-docs-ia\documentos_simulados
```

## Pruebas
```powershell
python -m unittest discover .\proyectos\03-simulador-drive-docs-ia\tests -v
```

## Límites
Sin Drive real, sin Docs real, sin OAuth real, sin APIs externas y sin IA real.

## 🪪 Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  
© 2025 – Txema Ríos. Todos los derechos compartidos.
