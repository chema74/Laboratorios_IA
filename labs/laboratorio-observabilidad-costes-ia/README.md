# Laboratorio de Observabilidad y Costes de IA (V2.1)

Laboratorio local y demostrable para analizar observabilidad, coste y riesgo operativo de sistemas de IA en contexto empresarial.

## Problema empresarial que resuelve

Los equipos que usan IA necesitan visibilidad rápida sobre coste, latencia, errores, concentración de consumo y riesgos de gobernanza para decidir mejoras sin depender de infraestructura compleja.

## Qué demuestra técnicamente

- Motor local de observabilidad sin red.
- Métricas agregadas por evento, caso de uso, modelo y proveedor.
- Alertas operativas y recomendaciones accionables.
- Análisis ejecutivo con Groq opcional y fallback local determinista.
- Dashboard local interactivo con escenarios y entrada JSON.
- Generación de evidencias en Markdown, JSON y HTML.
- Tests aislados sin dependencia de Internet o APIs externas.

## Demo rápida local (menos de 60 segundos)

```powershell
python scripts\generar_evidencias_v21.py
python scripts\dashboard_observabilidad_costes.py
```

Abrir en navegador: `http://127.0.0.1:8765`

## Uso sin Groq (fallback local)

```powershell
$env:OBSERVABILIDAD_MODO="fallback_local"
python scripts\generar_evidencias_v21.py
```

## Uso con Groq opcional

1. Crear `.env` local a partir de `.env.example` o exportar variables de entorno.
2. Configurar `GROQ_API_KEY` y opcionalmente `GROQ_MODEL`.
3. Ejecutar scripts de dashboard o evidencias.

```powershell
$env:GROQ_API_KEY="tu_clave"
$env:GROQ_MODEL="llama-3.1-8b-instant"
python scripts\generar_evidencias_v21.py
```

Si la llamada a Groq falla, el sistema vuelve automáticamente a `fallback_local`.

## Generación de evidencias

```powershell
python scripts\generar_evidencias_v21.py
```

Salidas esperadas en `evidencias\v2_1\`:

- `evidencia_observabilidad_costes_v21.md`
- `evidencia_observabilidad_costes_v21.json`
- `evidencia_observabilidad_costes_v21.html`

## Ejecución de tests

```powershell
python -m pytest -q
```

## Estructura principal

- `src/observabilidad_costes_ia/`: motor V2.1, escenarios, fallback, integración Groq opcional y orquestación.
- `scripts/dashboard_observabilidad_costes.py`: dashboard server-side local.
- `scripts/generar_evidencias_v21.py`: generador reproducible de evidencias.
- `tests/`: pruebas de V1/V2 y V2.1.
- `evidencias/v2_1/`: artefactos de evidencia de demo.

## Seguridad de claves

- No se incluyen claves reales en repositorio.
- `.env` está ignorado en `.gitignore`.
- `.env.example` contiene solo placeholders.
- Los tests no llaman a Groq real.

## Limitaciones explícitas

- Es un laboratorio demostrable, no una plataforma productiva de observabilidad.
- Los costes son estimados por evento simulado.
- El análisis LLM depende de disponibilidad externa cuando se usa Groq.
- El dashboard prioriza robustez local sobre sofisticación visual.

## Cierre V2.1

El repositorio queda preparado como demo técnica empresarial de observabilidad y costes de IA con operación local, capa LLM opcional y evidencias reproducibles.

Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  
© 2025 – Txema Ríos. Todos los derechos compartidos.
