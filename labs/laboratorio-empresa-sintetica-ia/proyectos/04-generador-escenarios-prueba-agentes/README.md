# 04-generador-escenarios-prueba-agentes

## Objetivo
Generador de Escenarios de Prueba para Agentes con alcance V1 (Version 1 - Versión 1) local mínimo. Produce casos sintéticos evaluables sin ejecutar agentes reales.

## Implementado en esta V1 local mínima
- Lectura de entradas (si existen):
  - datos_ejemplo/empresa_sintetica_demo/empresa_sintetica.json
  - datos_ejemplo/eventos_negocio_demo/eventos_negocio.json
  - datos_ejemplo/documentos_sinteticos_demo/indice_documentos.json
- Fallback interno mínimo para pruebas autónomas.
- Generación determinista por seed de tipos:
  - escenario_normal
  - escenario_ambiguo
  - escenario_limite
  - escenario_peligroso
  - escenario_privacidad
  - escenario_operativo
  - escenario_documental
- Campos obligatorios por escenario, incluyendo comportamiento esperado sin ejecución de agentes.
- Valores controlados para:
  - ccion_recomendada
  - 
ivel_dificultad
- Exportación de salidas:
  - escenarios_prueba_agentes.json
  - escenarios_prueba_agentes.csv
  - esumen_escenarios.json
  - escenarios_markdown/*.md
- CLI local y pruebas con pytest.

## Cómo ejecutar la demo
Desde la raíz del repositorio:

`ash
python proyectos/04-generador-escenarios-prueba-agentes/ejecutar_demo.py --seed 42 --escenarios-por-tipo 3
`

Parámetros opcionales:
- --entrada-empresa <ruta_json>
- --entrada-eventos <ruta_json>
- --entrada-documentos <ruta_json>
- --salida <carpeta>

## Entrada por defecto
- datos_ejemplo/empresa_sintetica_demo/empresa_sintetica.json
- datos_ejemplo/eventos_negocio_demo/eventos_negocio.json
- datos_ejemplo/documentos_sinteticos_demo/indice_documentos.json

## Salida por defecto
- datos_ejemplo/escenarios_prueba_agentes_demo/
  - escenarios_prueba_agentes.json
  - escenarios_prueba_agentes.csv
  - esumen_escenarios.json
  - escenarios_markdown/*.md

## Cómo ejecutar los tests
`ash
pytest proyectos/04-generador-escenarios-prueba-agentes/tests -q
`

## Límites actuales
- Escenarios sintéticos para evaluación interna.
- No se ejecutan agentes reales.
- No hay IA (Artificial Intelligence - Inteligencia Artificial) real implementada.
- No hay API (Application Programming Interface - Interfaz de Programación de Aplicaciones) productiva ni llamadas externas.
- No hay datos reales.
- No hay integraciones externas.
- No hay servicios de pago.

## Propósito de esta base
Este proyecto prepara la base técnica para evaluación futura de agentes en entorno controlado y reproducible.

##  Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  
(c) 2026 - Txema Ríos. Todos los derechos compartidos.

