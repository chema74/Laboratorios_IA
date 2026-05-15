# 07-gemelo-digital-operativo-ligero

## Objetivo
Gemelo Digital Operativo Ligero con alcance V1 (Version 1 - Versión 1) local mínimo. Consolida artefactos sintéticos previos en un estado operativo unificado, reproducible y orientado a portfolio técnico.

## Implementado en esta V1 local mínima
- Carga de entradas previas (si existen): empresa, eventos, documentos, escenarios, crisis, revisiones y registro de decisiones.
- Fallback interno mínimo para ejecución autónoma y tests.
- Construcción de estado operativo consolidado con:
  - identidad de empresa sintética
  - métricas operativas
  - estado por áreas
  - alertas operativas
  - decisiones simuladas
  - consecuencias operativas simuladas
  - línea temporal operativa
- Cálculo de índices:
  - indice_presion_operativa
  - indice_riesgo_simulado
  - indice_trazabilidad
- Exportación de salidas:
  - estado_operativo.json
  - metricas_operativas.json
  - metricas_operativas.csv
  - lertas_operativas.json
  - lertas_operativas.csv
  - decisiones_simuladas.json
  - decisiones_simuladas.csv
  - consecuencias_operativas.json
  - linea_tiempo_operativa.json
  - esumen_gemelo_digital.json
  - expediente_estado_operativo.md
- CLI local y pruebas con pytest.

## Cómo ejecutar la demo
Desde la raíz del repositorio:

`ash
python proyectos/07-gemelo-digital-operativo-ligero/ejecutar_demo.py --seed 42 --dias 10
`

## Entradas por defecto
- datos_ejemplo/empresa_sintetica_demo/empresa_sintetica.json
- datos_ejemplo/eventos_negocio_demo/eventos_negocio.json
- datos_ejemplo/documentos_sinteticos_demo/indice_documentos.json
- datos_ejemplo/escenarios_prueba_agentes_demo/escenarios_prueba_agentes.json
- datos_ejemplo/crisis_simuladas_demo/crisis_simuladas.json
- datos_ejemplo/revision_humana_demo/revisiones_humanas.json
- datos_ejemplo/revision_humana_demo/registro_decisiones.json

## Salida por defecto
- datos_ejemplo/gemelo_digital_operativo_demo/

## Cómo ejecutar los tests
`ash
pytest proyectos/07-gemelo-digital-operativo-ligero/tests -q
`

## Límites actuales
- El gemelo digital es sintético.
- No hay monitorización real.
- No hay toma de decisiones empresarial real.
- No se ejecutan agentes reales.
- No hay IA (Artificial Intelligence - Inteligencia Artificial) real implementada.
- No hay API (Application Programming Interface - Interfaz de Programación de Aplicaciones) productiva ni llamadas externas.
- No hay datos reales, integraciones externas ni servicios de pago.

## Propósito de esta base
Este proyecto prepara la base para dashboards locales futuros, evaluación de agentes, seguridad defensiva, Big Data empresarial y demo narrativa completa.

##  Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  
(c) 2026 - Txema Ríos. Todos los derechos compartidos.

