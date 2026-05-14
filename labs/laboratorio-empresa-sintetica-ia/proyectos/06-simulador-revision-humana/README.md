# 06-simulador-revision-humana

## Objetivo
Simulador de Revisión Humana con alcance V1 (Version 1 – Versión 1) local mínimo. Simula decisiones de revisión sobre artefactos sintéticos del laboratorio con trazabilidad reproducible.

## Implementado en esta V1 local mínima
- Lectura de entradas (si existen):
  - datos_ejemplo/eventos_negocio_demo/eventos_negocio.json
  - datos_ejemplo/documentos_sinteticos_demo/indice_documentos.json
  - datos_ejemplo/escenarios_prueba_agentes_demo/escenarios_prueba_agentes.json
  - datos_ejemplo/crisis_simuladas_demo/crisis_simuladas.json
- Fallback interno mínimo para ejecución y tests autónomos.
- Simulación determinista de revisiones sobre:
  - evento_negocio
  - documento_sintetico
  - escenario_prueba_agente
  - crisis_simulada
- Decisiones simuladas controladas:
  - ceptar, echazar, corregir, escalar, solicitar_mas_informacion, egistrar_incidente, loquear_accion
- Acciones posteriores controladas:
  - cerrar_revision, enviar_a_revision_senior, devolver_para_correccion, generar_informe, loquear_automatizacion, brir_incidencia, mantener_observacion
- Registro agregado de decisiones con trazabilidad.
- Exportación de artefactos:
  - evisiones_humanas.json
  - evisiones_humanas.csv
  - egistro_decisiones.json
  - egistro_decisiones.csv
  - esumen_revision_humana.json
  - expediente_revision_humana.md
- CLI local y tests con pytest.

## Cómo ejecutar la demo
Desde la raíz del repositorio:

`ash
python proyectos/06-simulador-revision-humana/ejecutar_demo.py --seed 42 --revisiones 20 --porcentaje-escalado 25
`

Parámetros opcionales:
- --entrada-eventos <ruta_json>
- --entrada-documentos <ruta_json>
- --entrada-escenarios <ruta_json>
- --entrada-crisis <ruta_json>
- --salida <carpeta>

## Salida por defecto
- datos_ejemplo/revision_humana_demo/
  - evisiones_humanas.json
  - evisiones_humanas.csv
  - egistro_decisiones.json
  - egistro_decisiones.csv
  - esumen_revision_humana.json
  - expediente_revision_humana.md

## Cómo ejecutar los tests
`ash
pytest proyectos/06-simulador-revision-humana/tests -q
`

## Límites actuales
- Revisiones sintéticas para evaluación interna.
- No hay revisión humana real.
- No hay validación profesional real.
- No se ejecutan agentes reales.
- No hay IA (Artificial Intelligence – Inteligencia Artificial) real implementada.
- No hay API (Application Programming Interface – Interfaz de Programación de Aplicaciones) productiva ni llamadas externas.
- No hay datos reales ni integraciones externas.
- No hay servicios de pago.

## Propósito de esta base
Este proyecto prepara la base para evaluación futura de agentes, trazabilidad, auditoría simulada y demos narrativas futuras.

## 🪪 Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  
© 2025 – Txema Ríos. Todos los derechos compartidos.
