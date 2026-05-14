# laboratorio-rag-corporativo-local

> **Estado**: V2.1 Ready · ✅ 20 tests passing · 🌍 PDF público integrado · 📄 Docs en castellano

Laboratorio **local, gratuito y reproducible** de RAG corporativo en castellano. La V2.1 mantiene el flujo local V2 y añade una capa LLM opcional con Groq, fallback determinista, evidencias rápidas y demo interactiva local.

## Demo en 3 pasos (sin configuración)

```powershell
# 1. Ingestar documento público real (1 PDF dummy de 13KB)
python scripts\demo_pdf_publico.py

# 2. Preparar índice y fragmentos
python scripts\sembrar_datos.py

# 3. Ejecutar pipeline + generar evidencias
python scripts\demo_llm_groq.py
python scripts\generar_panel_demo.py
```   

## Demo rápida V2.1

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
- Sin `GROQ_API_KEY`, con error de SDK/red o con `FORZAR_FALLBACK_LOCAL=1`: usa fallback local determinista.

## Demo interactiva local

```powershell
python scripts\servidor_demo_interactivo.py
```

URL local:

- `http://127.0.0.1:8767`

Uso:

- Selecciona una consulta de ejemplo o escribe una consulta propia.
- Marca `Usar Groq si hay GROQ_API_KEY` para intentar análisis remoto opcional.
- Marca `Forzar fallback local` para ejecutar siempre en local.
- Ejecuta la consulta y revisa respuesta, fragmentos recuperados y trazabilidad.

Evidencias por ejecución interactiva:

- Carpeta: `evidencias\interactivas\`
- Archivos:
  - `YYYYMMDD_HHMMSS_resultado.json`
  - `YYYYMMDD_HHMMSS_informe.md`

## Ejecución V2 base (preservada)

```powershell
python scripts\sembrar_datos.py
python scripts\comprobar_salud.py
python scripts\ejecutar_demo.py
python evaluacion\evaluacion_offline.py
python -m unittest discover tests -v
```

## Qué implementa

- Ingesta documental sintética (corpus corporativo JSON local).
- Segmentación en fragmentos trazables por documento y sección.
- Recuperación híbrida local (señal léxica + etiquetas/área).
- Reordenación de resultados recuperados.
- Respuestas extractivas con citas.
- Capa LLM opcional Groq con fallback local determinista.
- Trazabilidad de ejecución por etapas y por ruta LLM.
- Costes simulados por consulta.
- Evaluación offline con dataset dorado.
- Demo local CLI + demo interactiva local.

## Evidencias principales

- V2.1: `evidencias\README.md`, `evidencias\demo_llm_groq.md`, `evidencias\resultado_demo_llm_groq.json`, `evidencias\panel_demo.html`.
- Interactivas: `evidencias\interactivas\`.
- V2 base: `evaluacion\resultados\demo_rag_corporativo.md`, `evaluacion\resultados\resultado_evaluacion.md`.
- Validación funcional: suite `tests\`.

## Estructura y detalle

- Catálogo funcional: [CATALOGO.md](CATALOGO.md)
- Arquitectura implementada: [docs/ARQUITECTURA.md](docs/ARQUITECTURA.md)
- Guía de ejecución: [docs/GUIA_EJECUCION.md](docs/GUIA_EJECUCION.md)
- Decisiones técnicas: [docs/DECISIONES_TECNICAS.md](docs/DECISIONES_TECNICAS.md)
- Mapa de evidencias: [docs/MAPA_EVIDENCIAS.md](docs/MAPA_EVIDENCIAS.md)

## Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.

© 2026 – Txema Ríos.
