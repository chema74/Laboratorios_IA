# 02 - Simulador Defensivo de Prompt Injection (V1 local funcional mínima)

## Objetivo
Simular entradas sintéticas no accionables tipo prompt injection para evaluar clasificación defensiva, políticas y necesidad de revisión humana.

## Funcionalidad implementada en V1
- Carga y validación de entradas sintéticas y configuración defensiva.
- Verificación de placeholders ficticios no accionables.
- Clasificación defensiva por reglas locales.
- Activación de política defensiva asociada.
- Puntuación simulada por severidad y revisión humana.
- Resúmenes por categoría, severidad y políticas activadas.
- Generación de informe Markdown y JSON de resultados.

## Ejecución
```powershell
python .\proyectos\02-simulador-prompt-injection-defensivo\src\simulador_prompt_injection_defensivo.py --inputs .\proyectos\02-simulador-prompt-injection-defensivo\datos_ejemplo\entradas_prompt_injection_sinteticas.json --config .\proyectos\02-simulador-prompt-injection-defensivo\datos_ejemplo\configuracion_simulador_defensivo.json --output-md .\proyectos\02-simulador-prompt-injection-defensivo\informes\informe_simulacion_prompt_injection.md --output-json .\proyectos\02-simulador-prompt-injection-defensivo\informes\resultado_simulacion_prompt_injection.json
```

## 🪪 Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  
© 2025 – Txema Ríos. Todos los derechos compartidos.
