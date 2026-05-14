# Proyecto 10: Demo Google IA Empresarial Completa (V1 local funcional)

## Objetivo
Construir una demo integradora local de todo el laboratorio Google IA empresarial simulado.

## Alcance V1
- lectura de escenario y configuración sintéticos;
- narrativa empresarial y recorrido por 10 módulos;
- generación de guion, expediente, mapa de componentes y JSON de demo.

## Ejecución
```powershell
python .\proyectos\10-demo-google-ia-empresarial-completa\src\demo_google_ia_empresarial.py --scenario .\proyectos\10-demo-google-ia-empresarial-completa\datos_ejemplo\escenario_google_ia_empresarial.json --config .\proyectos\10-demo-google-ia-empresarial-completa\datos_ejemplo\configuracion_demo_google_ia.json --output-dir .\proyectos\10-demo-google-ia-empresarial-completa\demo
```

## Pruebas
```powershell
python -m unittest discover .\proyectos\10-demo-google-ia-empresarial-completa\tests -v
```

## Límites
Sin Google real, sin OAuth real, sin APIs externas, sin cloud y sin IA real.

## 🪪 Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  
© 2025 – Txema Ríos. Todos los derechos compartidos.
