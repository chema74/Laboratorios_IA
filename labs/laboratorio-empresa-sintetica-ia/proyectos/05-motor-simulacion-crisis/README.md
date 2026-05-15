# 05-motor-simulacion-crisis

## Objetivo
Motor de Simulación de Crisis con alcance V1 (Version 1 - Versión 1) local mínimo. Genera crisis empresariales ficticias para evaluación técnica y narrativa de laboratorio, sin uso operativo real.

## Implementado en esta V1 local mínima
- Lectura de entradas (si existen):
  - datos_ejemplo/empresa_sintetica_demo/empresa_sintetica.json
  - datos_ejemplo/eventos_negocio_demo/eventos_negocio.json
  - datos_ejemplo/documentos_sinteticos_demo/indice_documentos.json
  - datos_ejemplo/escenarios_prueba_agentes_demo/escenarios_prueba_agentes.json
- Fallback interno mínimo para ejecución y tests autónomos.
- Simulación determinista de tipos de crisis:
  - caida_ventas
  - uga_clientes
  - etraso_logistico
  - datos_corruptos
  - incidente_privacidad
  - saturacion_operativa
  - crisis_compuesta
- Línea temporal de crisis con hitos diarios simulados.
- Evaluación de impacto sintético y resumen consolidado.
- Exportación de artefactos:
  - crisis_simuladas.json
  - crisis_simuladas.csv
  - linea_tiempo_crisis.json
  - linea_tiempo_crisis.csv
  - esumen_crisis.json
  - expediente_crisis.md
- CLI local y pruebas con pytest.

## Cómo ejecutar la demo
Desde la raíz del repositorio:

`ash
python proyectos/05-motor-simulacion-crisis/ejecutar_demo.py --seed 42 --crisis 5 --dias 10
`

Parámetros opcionales:
- --entrada-empresa <ruta_json>
- --entrada-eventos <ruta_json>
- --entrada-documentos <ruta_json>
- --entrada-escenarios <ruta_json>
- --salida <carpeta>

## Salida por defecto
- datos_ejemplo/crisis_simuladas_demo/
  - crisis_simuladas.json
  - crisis_simuladas.csv
  - linea_tiempo_crisis.json
  - linea_tiempo_crisis.csv
  - esumen_crisis.json
  - expediente_crisis.md

## Cómo ejecutar los tests
`ash
pytest proyectos/05-motor-simulacion-crisis/tests -q
`

## Límites actuales
- Crisis sintéticas para pruebas internas del laboratorio.
- No se ejecutan agentes reales.
- No hay IA (Artificial Intelligence - Inteligencia Artificial) real implementada.
- No hay API (Application Programming Interface - Interfaz de Programación de Aplicaciones) productiva ni llamadas externas.
- No hay datos reales ni integraciones externas.
- No hay servicios de pago.
- No existe predicción real ni análisis empresarial real.

## Propósito de esta base
Este proyecto prepara base para simulaciones más avanzadas, evaluación de agentes, seguridad defensiva y demos narrativas futuras.

##  Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  
(c) 2026 - Txema Ríos. Todos los derechos compartidos.

