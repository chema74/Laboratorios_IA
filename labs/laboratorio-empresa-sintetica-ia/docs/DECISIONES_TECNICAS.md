# Decisiones Técnicas

## Python local

El repositorio usa Python para mantener una ejecución local, sencilla de auditar y sin dependencias de servicios externos.

## Datos sintéticos

Todos los datos, documentos, eventos, escenarios y crisis son ficticios. Esta decisión permite demostrar arquitectura sin exponer información real.

## Separación modular

La carpeta `proyectos/` divide el laboratorio en 10 piezas funcionales conectadas por la demo narrativa final.

## Validación con pytest

La validación global se ejecuta con:

```powershell
python -m pytest .\proyectos -q
```

## Exclusiones deliberadas

No se incorpora IA real, cloud obligatorio, APIs externas obligatorias ni servicios de pago. Esas capacidades quedan fuera de esta versión local.

## 🪪 Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  
© 2025 – Txema Ríos. Todos los derechos compartidos.
