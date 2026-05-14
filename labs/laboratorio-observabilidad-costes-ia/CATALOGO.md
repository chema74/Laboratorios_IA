# Catálogo V1

Catálogo de módulos del laboratorio de observabilidad y costes IA con su evidencia asociada.

## Aplicación

- `app/main.py`: entrada CLI para ejecutar flujo de observabilidad local.
Evidencia: ejecución de demo y generación de salida operativa.
- `app/config.py`: configuración de rutas y parámetros locales.
Evidencia: coherencia de rutas para datos, informe y panel.
- `app/modelos.py`: estructuras de datos para eventos y métricas.
Evidencia: intercambio consistente entre servicios y módulos de análisis.

## Observabilidad

- `observabilidad/trazador.py`: trazabilidad de eventos y etapas.
Evidencia: registro de trazas que sustentan auditoría local.
- `observabilidad/latencias.py`: cálculo de latencias por evento/flujo.
Evidencia: métricas de tiempo usadas en informe y panel.
- `observabilidad/costes_simulados.py`: cálculo de coste ficticio por consumo.
Evidencia: coste agregado reportado sin proveedores externos.
- `observabilidad/presupuesto.py`: control contra presupuesto operativo simulado.
Evidencia: señales de consumo respecto a umbrales definidos.
- `observabilidad/degradacion.py`: detección de degradación de servicio.
Evidencia: alertas/indicadores de caída de desempeño.
- `observabilidad/errores.py`: análisis de eventos de error.
Evidencia: resumen de incidencias y su impacto operativo.
- `observabilidad/feedback.py`: análisis de feedback sintético de usuarios.
Evidencia: indicadores de percepción de calidad de servicio.

## Servicios

- `servicios/simulador_eventos.py`: generación de secuencias sintéticas de uso IA.
Evidencia: eventos persistidos para análisis reproducible.
- `servicios/motor_observabilidad.py`: orquestación de métricas y reglas.
Evidencia: resultados consolidados para informe y panel.
- `servicios/generador_informes.py`: salida documental de resultados.
Evidencia: `informes/informe_observabilidad_costes_ia.md`.

## Datos y salidas

- `datos/eventos_ia_sinteticos.json`: eventos base de operación simulada.
- `datos/presupuesto_operativo.json`: presupuesto ficticio de referencia.
- `datos/feedback_usuarios.json`: percepciones sintéticas de usuarios.
- `panel/panel_observabilidad.html`: visualización local estática.

## Scripts y pruebas

- `scripts/sembrar_datos.py`: siembra de datos sintéticos.
- `scripts/comprobar_salud.py`: verificación de integridad operativa.
- `scripts/ejecutar_demo.py`: ejecución demo con salida resumida.
- `scripts/generar_panel.py`: generación/reconstrucción del panel local.
- `tests/`: validación unitaria de análisis y motor.

## 🪪 Licencia y Autoría

Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.

© 2025 – Txema Ríos. Todos los derechos compartidos.
