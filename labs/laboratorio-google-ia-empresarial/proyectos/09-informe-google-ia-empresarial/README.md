# Proyecto 09: Informe Google IA Empresarial (V1 local funcional)

## Objetivo
Generar un informe consolidado del laboratorio Google IA empresarial en modo local simulado.

## Alcance V1
- consolidación de resultados sintéticos de módulos 01 a 08;
- cálculo de puntuación global y nivel de madurez;
- fortalezas, riesgos, brechas y recomendaciones;
- generación de informe Markdown y JSON.

## Ejecución
```powershell
python .\proyectos\09-informe-google-ia-empresarial\src\generador_informe_google_ia.py --results .\proyectos\09-informe-google-ia-empresarial\datos_ejemplo\resultados_google_ia_empresarial.json --config .\proyectos\09-informe-google-ia-empresarial\datos_ejemplo\configuracion_informe_google_ia.json --output-md .\proyectos\09-informe-google-ia-empresarial\informes\informe_google_ia_empresarial.md --output-json .\proyectos\09-informe-google-ia-empresarial\informes\informe_google_ia_empresarial.json
```

## Pruebas
```powershell
python -m unittest discover .\proyectos\09-informe-google-ia-empresarial\tests -v
```

## Límites
Sin Google real, sin OAuth real, sin APIs externas, sin cloud y sin IA real.

##  Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  
(c) 2026 - Txema Ríos. Todos los derechos compartidos.

