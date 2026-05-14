# Demo LLM Groq V2.1

- Fecha UTC: 2026-05-13T07:01:02.779628+00:00
- Proveedor: fallback_local
- Modo: determinista
- Modelo: llama-3.1-8b-instant
- Motivo fallback: Error Groq (APIConnectionError): Connection error.

## Resumen
Fallback local activo. Casos=2, hallazgos_pii=9, riesgo=critico.

## Riesgos
- Nivel de riesgo detectado: critico
- Exposición residual posible en prompts no minimizados.
- Filtración en salida si no se aplica bloqueo automático.

## Recomendaciones
- Aplicar anonimización previa a cualquier intercambio externo.
- Reducir campos no necesarios en prompts antes del procesamiento.
- Mantener validación de salida para bloquear PII de severidad alta.

## Trazabilidad LLM
- groq_api_key_activa: True
- forzar_fallback_local: False
- groq_model: llama-3.1-8b-instant
- sdk_groq_disponible: True
- opener_personalizado: False
- ruta_ejecucion: groq_sdk

## Trazabilidad
- Casos analizados: 2
- Riesgo motor base: critico

## Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.

© 2026 – Txema Ríos.