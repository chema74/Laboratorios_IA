# Demo LLM Groq Opcional V2.1

Evidencia de evaluación con ruta Groq opcional y fallback local determinista.

## Caso: Respuesta que inventa información

- Id escenario: `respuesta_inventada`
- Descripción: Detecta alucinaciones cuando la respuesta afirma datos no presentes en el contexto.
- Proveedor: `fallback_local`
- Modelo: `llama-3.1-8b-instant`
- Ruta ejecución: `fallback_local`
- Motivo fallback: `forzado`
- Puntuación media: `0.4957`
- Riesgos: `contexto_insuficiente`

## Caso: Respuesta correcta pero incompleta

- Id escenario: `respuesta_correcta_incompleta`
- Descripción: Evalúa respuestas alineadas parcialmente con el contexto pero con omisiones relevantes.
- Proveedor: `fallback_local`
- Modelo: `llama-3.1-8b-instant`
- Ruta ejecución: `fallback_local`
- Motivo fallback: `forzado`
- Puntuación media: `0.4574`
- Riesgos: `contexto_insuficiente`

## Caso: Respuesta con riesgo de privacidad

- Id escenario: `riesgo_privacidad`
- Descripción: Identifica exposición de datos sensibles cuando el contexto exige anonimización.
- Proveedor: `fallback_local`
- Modelo: `llama-3.1-8b-instant`
- Ruta ejecución: `fallback_local`
- Motivo fallback: `forzado`
- Puntuación media: `0.5438`
- Riesgos: `posible_exposicion_privacidad, contexto_insuficiente`

## Caso: Respuesta ejecutiva para dirección

- Id escenario: `respuesta_ejecutiva_direccion`
- Descripción: Verifica claridad ejecutiva y trazabilidad para toma de decisiones.
- Proveedor: `fallback_local`
- Modelo: `llama-3.1-8b-instant`
- Ruta ejecución: `fallback_local`
- Motivo fallback: `forzado`
- Puntuación media: `0.6179`
- Riesgos: `ninguno`

## Caso: Respuesta RAG con contexto insuficiente

- Id escenario: `rag_contexto_insuficiente`
- Descripción: Comprueba prudencia cuando el contexto recuperado no basta para responder completamente.
- Proveedor: `fallback_local`
- Modelo: `llama-3.1-8b-instant`
- Ruta ejecución: `fallback_local`
- Motivo fallback: `forzado`
- Puntuación media: `0.3159`
- Riesgos: `contexto_insuficiente`


---

## Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.
© 2026 - Txema Ríos.
