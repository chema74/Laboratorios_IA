# Mapa de Evidencias

Relación entre capacidades declaradas y artefactos reales del repositorio.

## 1. Tareas enterprise sintéticas

- Evidencia: `datos/tareas_enterprise.json`
- Generación/actualización: `python scripts\sembrar_datos.py`

## 2. Herramientas simuladas

- Evidencia: `datos/herramientas_simuladas.json`
- Generación/actualización: `python scripts\sembrar_datos.py`

## 3. Políticas y límites de agentes

- Evidencia: `datos/politicas_agentes.json`
- Generación/actualización: `python scripts\sembrar_datos.py`

## 4. Escenarios de coordinación multiagente

- Evidencia: `datos/escenarios_multiagente.json`
- Generación/actualización: `python scripts\sembrar_datos.py`

## 5. Informe de demo

- Evidencia: `informes/demo_agentes_enterprise.md`
- Generación: `python scripts\ejecutar_demo.py`

## 6. Informe de escenario multiagente

- Evidencia: `informes/escenario_multiagente.md`
- Generación: `python scripts\ejecutar_escenario_multiagente.py`

## 7. Calidad funcional

- Evidencia: suite `tests/`
- Ejecución: `python -m unittest discover tests -v`

## Alcance V1

No se incluyen evidencias de acciones reales, conexión a servicios corporativos ni automatización productiva porque no forman parte de la implementación actual.

## 🪪 Licencia y Autoría

Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.

© 2025 – Txema Ríos. Todos los derechos compartidos.
