# Guía de Ejecución

Orden recomendado en Windows PowerShell desde la raíz del repositorio.

## 1. Sembrar datos sintéticos

```powershell
python scripts\sembrar_datos.py
```

## 2. Comprobar salud

```powershell
python scripts\comprobar_salud.py
```

## 3. Ejecutar demo

```powershell
python scripts\ejecutar_demo.py
```

## 4. Generar informe de privacidad

```powershell
python scripts\generar_informe_privacidad.py
```

Salida principal:
- `informes\informe_privacidad_datos_ia.md`

## 5. Ejecutar tests

```powershell
python -m unittest discover tests -v
```

## Notas operativas

- Flujo local y reproducible, sin servicios externos.
- Si hay incoherencias, repetir siembra y chequeo antes de regenerar informe.

## 🪪 Licencia y Autoría

Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.

© 2025 – Txema Ríos. Todos los derechos compartidos.
