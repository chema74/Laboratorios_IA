# Evidencia V2.1 - Observabilidad y Costes IA

- Escenario: `uso_normal_controlado`
- Modo: `fallback_local`
- Timestamp: `2026-05-14T10:15:35Z`

## Resumen ejecutivo
Se analizaron 3 eventos con coste total estimado de 0.0370 EUR, latencia media de 620.0 ms y tasa de errores de 0.00%.

## Diagnóstico Groq / modo de ejecución
```json
{
  "solicitado": false,
  "estado": "no_solicitado",
  "categoria": "modo_fallback_forzado",
  "http_status": null,
  "modelo_usado": null,
  "mensaje_seguro": "El análisis se ejecutó en modo fallback local por configuración."
}
```

## Métricas agregadas
```json
{
  "total_eventos": 3,
  "coste_total_estimado": 0.037,
  "coste_por_caso_uso": {
    "atencion_cliente": 0.012,
    "cumplimiento": 0.015,
    "soporte_tic": 0.01
  },
  "tokens_totales": 2230,
  "latencia_media_ms": 620,
  "tasa_errores": 0.0,
  "eventos_riesgo": 0,
  "proveedores_mas_usados": {
    "local": 3
  },
  "modelos_mas_usados": {
    "llama-3.1-8b": 3
  },
  "alertas": [],
  "recomendaciones_operativas": [
    "Operación estable en la muestra. Mantener monitorización diaria."
  ]
}
```

## Alertas
- Sin alertas

## Recomendaciones
### Coste
- Definir topes de tokens por operación.
- Priorizar modelos más eficientes para tareas repetitivas.
### Operación
- Revisar alertas diariamente con responsable técnico.
- Mantener trazabilidad por evento y equipo.
### Gobernanza
- Gobernanza operativa dentro de umbrales de laboratorio.


Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  
© 2025 – Txema Ríos. Todos los derechos compartidos.
