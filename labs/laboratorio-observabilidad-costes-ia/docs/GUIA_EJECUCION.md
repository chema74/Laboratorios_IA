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

## 4. Generar panel HTML local

```powershell
python scripts\generar_panel.py
```

Salidas clave:
- `informes\informe_observabilidad_costes_ia.md`
- `panel\panel_observabilidad.html`

## 5. Ejecutar tests

```powershell
python -m unittest discover tests -v
```

## Notas

- Toda la ejecución es local, sin cloud ni APIs externas.
- Si hay inconsistencias, repetir siembra y chequeo antes de regenerar panel.

##  Licencia y Autoría

Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.

(c) 2026 - Txema Ríos. Todos los derechos compartidos.

