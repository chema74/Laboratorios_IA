# Proyecto 01: Mapa del Ecosistema Google IA (V1 local funcional)

## Objetivo
Mapear técnicamente el ecosistema Google orientado a IA empresarial mediante datos sintéticos y reglas de validación local.

## Alcance V1
- carga y validación de componentes simulados;
- clasificación por categoría y capa arquitectónica;
- detección de extensiones V2 opcionales;
- generación de informe Markdown y salida JSON.

## Ejecución
```powershell
python .\proyectos\01-mapa-ecosistema-google-ia\src\generador_mapa_ecosistema.py --ecosystem .\proyectos\01-mapa-ecosistema-google-ia\datos_ejemplo\ecosistema_google_ia_sintetico.json --config .\proyectos\01-mapa-ecosistema-google-ia\datos_ejemplo\configuracion_mapa_google_ia.json --output-md .\proyectos\01-mapa-ecosistema-google-ia\informes\informe_mapa_ecosistema_google_ia.md --output-json .\proyectos\01-mapa-ecosistema-google-ia\informes\mapa_ecosistema_google_ia.json
```

## Pruebas
```powershell
python -m unittest discover .\proyectos\01-mapa-ecosistema-google-ia\tests -v
```

## Límites
Sin Google real, sin OAuth real, sin APIs reales, sin cloud obligatorio y sin IA real.

##  Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  
(c) 2026 - Txema Ríos. Todos los derechos compartidos.

