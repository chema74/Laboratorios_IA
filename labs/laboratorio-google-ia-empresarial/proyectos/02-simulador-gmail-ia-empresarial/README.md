# Proyecto 02: Simulador Gmail IA Empresarial (V1 local funcional)

## Objetivo
Simular un flujo empresarial de correo con clasificación, prioridad, sugerencias de respuesta y tareas, sin usar Gmail real ni IA real.

## Alcance V1
- carga y validación de correos sintéticos;
- clasificación por reglas locales;
- generación de respuesta y tarea simulada;
- creación de registro JSON por correo en bandeja local;
- generación de informe Markdown y resultado JSON.

## Ejecución
```powershell
python .\proyectos\02-simulador-gmail-ia-empresarial\src\simulador_gmail_ia.py --emails .\proyectos\02-simulador-gmail-ia-empresarial\datos_ejemplo\correos_empresariales_sinteticos.json --config .\proyectos\02-simulador-gmail-ia-empresarial\datos_ejemplo\configuracion_gmail_simulado.json --output-md .\proyectos\02-simulador-gmail-ia-empresarial\informes\informe_gmail_ia_simulado.md --output-json .\proyectos\02-simulador-gmail-ia-empresarial\informes\resultado_gmail_ia_simulado.json --mailbox-dir .\proyectos\02-simulador-gmail-ia-empresarial\bandeja_simulada
```

## Pruebas
```powershell
python -m unittest discover .\proyectos\02-simulador-gmail-ia-empresarial\tests -v
```

## Límites
Sin Gmail real, sin OAuth real, sin Gmail API, sin cloud obligatorio y sin modelos LLM reales.

##  Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  
(c) 2026 - Txema Ríos. Todos los derechos compartidos.

