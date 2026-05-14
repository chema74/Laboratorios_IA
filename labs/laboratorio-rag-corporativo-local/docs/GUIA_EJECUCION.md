# Guía de Ejecución

Secuencia recomendada en Windows PowerShell para reproducir la V1 completa.

## 1. Sembrar datos sintéticos

```powershell
python scripts\sembrar_datos.py
```

## 2. Comprobar salud del repositorio

```powershell
python scripts\comprobar_salud.py
```

## 3. Ejecutar demo local

```powershell
python scripts\ejecutar_demo.py
```

Salida esperada principal:
- `evaluacion\resultados\demo_rag_corporativo.md`

## 4. Ejecutar evaluación offline

```powershell
python evaluacion\evaluacion_offline.py
```

Salida esperada principal:
- `evaluacion\resultados\resultado_evaluacion.md`

## 5. Ejecutar tests

```powershell
python -m unittest discover tests -v
```

## Notas de operación

- Ejecutar los comandos desde la raíz del repositorio.
- Si faltan resultados, repetir primero la siembra de datos y la comprobación de salud.
- La ejecución es 100% local, sin cloud ni APIs externas.

## 🪪 Licencia y Autoría

Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.

© 2025 – Txema Ríos. Todos los derechos compartidos.
