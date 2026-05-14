# Mapa de Evidencias

Vinculación entre capacidades declaradas y artefactos reales generados por el laboratorio.

## 1. Eventos sintéticos de uso IA

- Evidencia: `datos/eventos_ia_sinteticos.json`
- Generación/actualización: `python scripts\sembrar_datos.py`

## 2. Presupuesto operativo ficticio

- Evidencia: `datos/presupuesto_operativo.json`
- Generación/actualización: `python scripts\sembrar_datos.py`

## 3. Feedback sintético de usuarios

- Evidencia: `datos/feedback_usuarios.json`
- Generación/actualización: `python scripts\sembrar_datos.py`

## 4. Informe de observabilidad y costes

- Evidencia principal: `informes/informe_observabilidad_costes_ia.md`
- Generación: `python scripts\ejecutar_demo.py`

## 5. Panel HTML local

- Evidencia principal: `panel/panel_observabilidad.html`
- Generación: `python scripts\generar_panel.py`

## 6. Calidad funcional

- Evidencia: suite `tests/`
- Ejecución: `python -m unittest discover tests -v`

## Alcance V1

No se incluyen evidencias de métricas reales de proveedor, cloud ni herramientas externas de observabilidad porque no forman parte de la implementación actual.

## 🪪 Licencia y Autoría

Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.

© 2025 – Txema Ríos. Todos los derechos compartidos.
