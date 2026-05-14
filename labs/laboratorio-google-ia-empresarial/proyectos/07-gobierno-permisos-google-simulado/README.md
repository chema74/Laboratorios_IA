# Proyecto 07: Gobierno de Permisos Google Simulado (V1 local funcional)

## Objetivo
Simular evaluación defensiva de permisos en un entorno Google empresarial ficticio.

## Alcance V1
- carga y validación de permisos sintéticos;
- evaluación de mínimo privilegio y riesgo;
- detección de permisos excesivos y revisión;
- decisión de gobierno: mantener, revisar, reducir o revocar;
- registros locales, informe Markdown y salida JSON.

## Ejecución
```powershell
python .\proyectos\07-gobierno-permisos-google-simulado\src\gobierno_permisos_google.py --permissions .\proyectos\07-gobierno-permisos-google-simulado\datos_ejemplo\permisos_google_simulados.json --config .\proyectos\07-gobierno-permisos-google-simulado\datos_ejemplo\configuracion_gobierno_permisos.json --output-md .\proyectos\07-gobierno-permisos-google-simulado\informes\informe_gobierno_permisos_google.md --output-json .\proyectos\07-gobierno-permisos-google-simulado\informes\resultado_gobierno_permisos_google.json --registry-dir .\proyectos\07-gobierno-permisos-google-simulado\registros
```

## Pruebas
```powershell
python -m unittest discover .\proyectos\07-gobierno-permisos-google-simulado\tests -v
```

## Límites
Sin Google real, sin OAuth real, sin APIs externas, sin cloud y sin IA real.

## 🪪 Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  
© 2025 – Txema Ríos. Todos los derechos compartidos.
