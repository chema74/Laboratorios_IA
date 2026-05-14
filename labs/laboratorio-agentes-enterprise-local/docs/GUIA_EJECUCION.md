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

## 4. Ejecutar escenario multiagente

```powershell
python scripts\ejecutar_escenario_multiagente.py
```

Salidas clave:
- `informes\demo_agentes_enterprise.md`
- `informes\escenario_multiagente.md`

## 5. Ejecutar tests

```powershell
python -m unittest discover tests -v
```

## Notas operativas

- Ejecución completamente local y determinista.
- Si aparecen incoherencias, repetir siembra y chequeo antes de reintentar demo/escenario.

## 🪪 Licencia y Autoría

Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.

© 2025 – Txema Ríos. Todos los derechos compartidos.
