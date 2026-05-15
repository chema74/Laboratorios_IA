# 09-comparador-agente-proceso

## Objetivo
Comparador entre Agente y Proceso con alcance V1 (Version 1 - Versión 1) local mínimo. Compara flujos manual, automatizado clásico y asistido por agente simulado sobre procesos empresariales ficticios.

## Implementado en esta V1 local mínima
- Carga de contexto multi-proyecto desde JSON con fallback interno.
- Catálogo de procesos empresariales sintéticos comparables.
- Simulación determinista de tres flujos:
  - manual
  - utomatizado_clasico
  - sistido_por_agente
- Cálculo de métricas simuladas por flujo:
  - tiempo estimado
  - errores simulados
  - trazabilidad
  - consistencia
  - carga de revisión humana
  - riesgo residual
  - coste relativo
  - resultado simulado
- Comparación por proceso con recomendación simulada controlada.
- Exportación JSON/CSV + resumen + expediente Markdown.

## Cómo ejecutar la demo
Desde la raíz del repositorio:

`ash
python proyectos/09-comparador-agente-proceso/ejecutar_demo.py --seed 42 --procesos 7
`

## Entradas por defecto
- datos_ejemplo/empresa_sintetica_demo/empresa_sintetica.json
- datos_ejemplo/eventos_negocio_demo/eventos_negocio.json
- datos_ejemplo/documentos_sinteticos_demo/indice_documentos.json
- datos_ejemplo/escenarios_prueba_agentes_demo/escenarios_prueba_agentes.json
- datos_ejemplo/crisis_simuladas_demo/crisis_simuladas.json
- datos_ejemplo/revision_humana_demo/revisiones_humanas.json
- datos_ejemplo/revision_humana_demo/registro_decisiones.json
- datos_ejemplo/gemelo_digital_operativo_demo/estado_operativo.json
- datos_ejemplo/gemelo_digital_operativo_demo/alertas_operativas.json
- datos_ejemplo/gemelo_digital_operativo_demo/decisiones_simuladas.json
- datos_ejemplo/privacidad_datos_sinteticos_demo/inventario_datos_sinteticos.json
- datos_ejemplo/privacidad_datos_sinteticos_demo/riesgos_privacidad_simulados.json

## Salida por defecto
- datos_ejemplo/comparador_agente_proceso_demo/
  - procesos_comparados.json
  - procesos_comparados.csv
  - esultados_flujos.json
  - esultados_flujos.csv
  - comparaciones_agente_proceso.json
  - comparaciones_agente_proceso.csv
  - esumen_comparador.json
  - expediente_comparador_agente_proceso.md

## Cómo ejecutar los tests
`ash
pytest proyectos/09-comparador-agente-proceso/tests -q
`

## Límites actuales
- Datos y métricas totalmente sintéticas.
- No hay benchmark real.
- No hay recomendación empresarial real.
- No se ejecutan agentes reales.
- No hay IA (Artificial Intelligence - Inteligencia Artificial) real implementada.
- No hay API (Application Programming Interface - Interfaz de Programación de Aplicaciones) productiva ni llamadas externas.
- No hay datos reales ni integraciones externas ni servicios de pago.

## Propósito de esta base
Este proyecto prepara la base para evaluación de agentes, AgentOps, consultoría técnica simulada y demo narrativa completa.

##  Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  
(c) 2026 - Txema Ríos. Todos los derechos compartidos.

