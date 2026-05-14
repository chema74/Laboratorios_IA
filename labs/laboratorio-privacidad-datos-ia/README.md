# laboratorio-privacidad-datos-ia

Laboratorio **local, gratuito y reproducible** de privacidad aplicada a sistemas de IA. Esta V2 mantiene el flujo base existente y añade una capa LLM opcional para demostraciones técnicas.

> Repositorio técnico y orientativo. **No constituye asesoramiento legal definitivo**.

## Demo rápida V2.1

Pensada para reclutadores y clientes técnicos que quieran ver el flujo completo en minutos.

```powershell
python scripts\sembrar_datos.py
python scripts\demo_llm_groq.py
python scripts\generar_panel_demo.py
```

Resultado esperado:

- `evidencias\resultado_demo_llm_groq.json`
- `evidencias\demo_llm_groq.md`
- `evidencias\panel_demo.html`

Comportamiento LLM:

- Con `GROQ_API_KEY`: intenta análisis opcional con Groq.
- Sin `GROQ_API_KEY` o si Groq falla: usa fallback local determinista.

## Demo interactiva local

Permite probar textos sintéticos propios desde navegador, ver minimización/anonimización y generar evidencias por ejecución.

```powershell
python scripts\servidor_demo_interactivo.py
```

URL local:

- `http://127.0.0.1:8766`

Uso:

- Selecciona un caso de ejemplo o pega texto sintético en la caja.
- Marca `Usar Groq si hay GROQ_API_KEY` para intentar análisis remoto opcional.
- Marca `Forzar fallback local` para ejecutar sin Groq aunque exista clave.
- Pulsa `Analizar privacidad` para ver resultado y trazabilidad.

Evidencias interactivas generadas:

- Carpeta: `evidencias\interactivas\`
- Archivos por ejecución:
  - `YYYYMMDD_HHMMSS_resultado.json`
  - `YYYYMMDD_HHMMSS_informe.md`

## Ejecución V2 base (preservada)

```powershell
python scripts\sembrar_datos.py
python scripts\comprobar_salud.py
python scripts\ejecutar_demo.py
python scripts\generar_informe_privacidad.py
python -m unittest discover tests -v
```

## Capacidades implementadas

- Dataset sintético con PII ficticia.
- Detección de PII.
- Anonimización.
- Seudonimización.
- Minimización de contexto.
- Evaluación de exposición.
- Validación de salidas.
- Registro de tratamiento sintético.
- Informe Markdown de privacidad.
- Análisis LLM opcional con fallback determinista.

## Evidencias principales

- Informe base: `informes\informe_privacidad_datos_ia.md`.
- Evidencias V2.1: `evidencias\README.md`, `evidencias\demo_llm_groq.md`, `evidencias\resultado_demo_llm_groq.json`, `evidencias\panel_demo.html`.
- Validación funcional: suite `tests\`.

## Documentación principal

- Catálogo: [CATALOGO.md](CATALOGO.md)
- Arquitectura: [docs/ARQUITECTURA.md](docs/ARQUITECTURA.md)
- Guía de ejecución: [docs/GUIA_EJECUCION.md](docs/GUIA_EJECUCION.md)
- Integración LLM V2.1: [docs/INTEGRACION_LLM_GROQ_V2_1.md](docs/INTEGRACION_LLM_GROQ_V2_1.md)
- Decisiones técnicas: [docs/DECISIONES_TECNICAS.md](docs/DECISIONES_TECNICAS.md)
- Mapa de evidencias: [docs/MAPA_EVIDENCIAS.md](docs/MAPA_EVIDENCIAS.md)
- Límites legales y supuestos: [docs/LIMITES_LEGALES_Y_SUPUESTOS.md](docs/LIMITES_LEGALES_Y_SUPUESTOS.md)

## Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.

© 2026 – Txema Ríos.
