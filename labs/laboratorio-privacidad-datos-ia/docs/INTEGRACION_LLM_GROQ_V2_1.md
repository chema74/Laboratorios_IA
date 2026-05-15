# Integración LLM Groq V2.1

## Objetivo

Añadir una capa LLM opcional para enriquecer la demo sin romper el laboratorio V2 base ni forzar dependencias de red en pruebas unitarias.

## Componentes añadidos

- `servicios/analisis_llm.py`
- `scripts/demo_llm_groq.py`
- `scripts/generar_panel_demo.py`
- `.env.example`
- `tests/test_analisis_llm.py`

## Decisión técnica

1. Groq solo se usa si existe variable de entorno `GROQ_API_KEY`.
2. Si no existe `GROQ_API_KEY` o la llamada falla, se activa fallback local determinista.
3. Los tests no requieren Internet ni credenciales reales.

## Flujo funcional V2.1

1. Entrada con datos personales sintéticos.
2. Detección, minimización, anonimización y seudonimización con el motor existente.
3. Resumen estructurado para capa LLM opcional.
4. Análisis Groq (si hay clave) o fallback local (si no hay clave o hay error).
5. Generación de informe Markdown y panel HTML de revisión rápida.

## Ejecución demo V2.1

```powershell
python scripts\demo_llm_groq.py
python scripts\generar_panel_demo.py
```

Archivos generados:

- `evidencias\resultado_demo_llm_groq.json`
- `evidencias\demo_llm_groq.md`
- `evidencias\panel_demo.html`

## Pruebas

```powershell
python -m unittest discover tests -v
```

Cobertura nueva:

- Fallback sin clave.
- Camino Groq simulado correcto.
- Fallback por error de proveedor.

## Variables de entorno

`.env.example` incluye:

```env
GROQ_API_KEY=
```

Sin claves reales en repositorio.

## Compatibilidad

- No modifica la web pública.
- No elimina funcionalidad existente.
- Mantiene el flujo local de la V2 actual.

## Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.

© 2026 - Txema Ríos.

