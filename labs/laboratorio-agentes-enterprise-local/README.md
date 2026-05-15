# laboratorio-agentes-enterprise-local

Laboratorio **local, gratuito y reproducible** de agentes enterprise de IA, orientado a demostrar coordinación controlada, trazabilidad y evaluación en un entorno sintético. Esta V1 permite ensayar planificación, ejecución simulada y revisión multiagente sin dependencias externas.

## Problema empresarial que simula

Simula operaciones donde varios agentes deben colaborar con control: planificación de tareas, selección de herramientas, memoria operativa, límites de acción y revisión trazable antes de automatizar procesos reales.

## Capacidades implementadas en V1

- Tareas enterprise sintéticas.
- Agente planificador.
- Agente ejecutor.
- Agente revisor.
- Agente coordinador.
- Herramientas simuladas.
- Memoria operativa.
- Límites de acción.
- Orquestación multiagente.
- Evaluación de resultados.
- Trazabilidad de decisiones y ejecución.
- Costes simulados.
- Informes Markdown.

## Límites explícitos de la V1

- Sin LLM externo.
- Sin acciones reales.
- Sin conexión a CRM real.
- Sin correos reales.
- Sin calendarios reales.
- Sin automatización productiva.
- Sin datos reales.

## Ejecución rápida (Windows PowerShell)

```powershell
python scripts\sembrar_datos.py
python scripts\comprobar_salud.py
python scripts\ejecutar_demo.py
python scripts\ejecutar_escenario_multiagente.py
python -m unittest discover tests -v
```

## Evidencias principales

- Informe demo: `informes\demo_agentes_enterprise.md`.
- Informe multiagente: `informes\escenario_multiagente.md`.
- Datos base: `datos\tareas_enterprise.json`, `datos\herramientas_simuladas.json`, `datos\politicas_agentes.json`, `datos\escenarios_multiagente.json`.
- Validación funcional: suite `tests\`.

## Documentación principal

- Catálogo: [CATALOGO.md](CATALOGO.md)
- Arquitectura: [docs/ARQUITECTURA.md](docs/ARQUITECTURA.md)
- Guía de ejecución: [docs/GUIA_EJECUCION.md](docs/GUIA_EJECUCION.md)
- Decisiones técnicas: [docs/DECISIONES_TECNICAS.md](docs/DECISIONES_TECNICAS.md)
- Mapa de evidencias: [docs/MAPA_EVIDENCIAS.md](docs/MAPA_EVIDENCIAS.md)

##  Licencia y Autoría

Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.

(c) 2026 - Txema Ríos. Todos los derechos compartidos.

