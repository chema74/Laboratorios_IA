# laboratorio-evaluacion-llm-local

## Demo rápida V2.1

Este laboratorio evalúa respuestas LLM en castellano con enfoque reproducible local. La V2.1 añade una capa LLM opcional con Groq y fallback local determinista, sin romper la V2 offline existente.

### Ejecutar demo con fallback local

```powershell
python scripts\demo_llm_groq.py
python scripts\generar_panel_demo.py
```

Si no hay `GROQ_API_KEY`, o falla SDK/conexión, se aplica fallback local automáticamente.

### Ejecutar demo con Groq (opcional)

1. Configura `.env` o variables de entorno:

```powershell
$env:GROQ_API_KEY="tu_clave"
$env:GROQ_MODEL="llama-3.1-8b-instant"
```

2. Ejecuta:

```powershell
python scripts\demo_llm_groq.py
python scripts\generar_panel_demo.py
```

### Abrir dashboard interactivo local

```powershell
python scripts\servidor_demo_interactivo.py
```

Abrir: `http://127.0.0.1:8768`

Opcional self-test:

```powershell
python scripts\servidor_demo_interactivo.py --self-test
```

### Evidencias

- `evidencias/resultado_demo_llm_groq.json`
- `evidencias/demo_llm_groq.md`
- `evidencias/panel_demo.html`
- `evidencias/interactivas/`

### Garantías de ejecución

- Groq es opcional.
- Los tests no dependen de cloud.
- La suite normal no debe llamar a Internet.

## Ejecución base V2 (se conserva)

```powershell
python scripts\sembrar_datos.py
python scripts\comprobar_salud.py
python scripts\ejecutar_demo.py
python scripts\ejecutar_evaluacion.py
python -m unittest discover tests -v
```

## Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.
© 2026 - Txema Ríos.
