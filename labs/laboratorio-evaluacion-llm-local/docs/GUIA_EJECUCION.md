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

## 3. Ejecutar demo local

```powershell
python scripts\ejecutar_demo.py
```

## 4. Ejecutar evaluación completa

```powershell
python scripts\ejecutar_evaluacion.py
```

Salida principal esperada:
- `evaluacion\resultados\informe_evaluacion_llm.md`

## 5. Ejecutar tests

```powershell
python -m unittest discover tests -v
```

## Notas operativas

- Toda la ejecución es local y offline.
- Si hay incoherencias, repetir primero siembra de datos y chequeo de salud.

##  Licencia y Autoría

Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.

(c) 2026 - Txema Ríos. Todos los derechos compartidos.

