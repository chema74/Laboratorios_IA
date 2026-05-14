# Proyecto 06: Conector Gemini Fallback Local (V1 local funcional)

## Objetivo
Implementar un conector conceptual que ejecute siempre fallback local sin uso de Gemini API real ni red.

## Alcance V1
- carga y validación de solicitudes sintéticas;
- verificación de modo V1 fallback-local;
- respuesta simulada determinista por tipo;
- trazabilidad de fallback y registro local por solicitud;
- informe Markdown y salida JSON.

## Ejecución
```powershell
python .\proyectos\06-conector-gemini-fallback-local\src\conector_gemini_fallback.py --requests .\proyectos\06-conector-gemini-fallback-local\datos_ejemplo\solicitudes_gemini_simuladas.json --config .\proyectos\06-conector-gemini-fallback-local\datos_ejemplo\configuracion_gemini_fallback.json --output-md .\proyectos\06-conector-gemini-fallback-local\informes\informe_gemini_fallback_local.md --output-json .\proyectos\06-conector-gemini-fallback-local\informes\resultado_gemini_fallback_local.json --responses-dir .\proyectos\06-conector-gemini-fallback-local\respuestas_simuladas
```

## Pruebas
```powershell
python -m unittest discover .\proyectos\06-conector-gemini-fallback-local\tests -v
```

## Límites
Sin Gemini API real, sin claves reales, sin OAuth real, sin red y sin IA real.

## 🪪 Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  
© 2025 – Txema Ríos. Todos los derechos compartidos.
