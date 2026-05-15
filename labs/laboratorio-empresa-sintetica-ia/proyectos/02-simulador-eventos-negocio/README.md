# 02-simulador-eventos-negocio

## Objetivo
Simulador de Eventos de Negocio con alcance V1 (Version 1 - Versión 1) local mínimo. Convierte una empresa sintética en secuencias de actividad operativa ficticia.

## Implementado en esta V1 local mínima
- Lectura de empresa sintética desde:
  - datos_ejemplo/empresa_sintetica_demo/empresa_sintetica.json (por defecto).
- Fallback interno mínimo si no existe archivo de entrada, para no depender de ejecución previa del proyecto 01.
- Simulación determinista por seed de estos tipos de evento:
  - pedido_creado
  - pago_recibido
  - pago_pendiente
  - devolucion_solicitada
  - eclamacion_cliente
  - etraso_operativo
  - cambio_estado_cliente
  - lerta_operativa
- Exportación de salidas:
  - eventos_negocio.json
  - eventos_negocio.csv
  - esumen_eventos.json
- CLI para configurar seed, días, volumen de eventos, entrada y salida.
- Tests con pytest para estructura, reproducibilidad, exportación y límites.

## Cómo ejecutar la demo
Desde la raíz del repositorio:

`ash
python proyectos/02-simulador-eventos-negocio/ejecutar_demo.py --seed 42 --dias 7 --eventos-por-dia 8
`

Parámetros opcionales:
- --entrada-empresa <ruta_json>
- --salida <carpeta>

Salida por defecto:
- datos_ejemplo/eventos_negocio_demo/

## Cómo ejecutar los tests
Desde la raíz del repositorio:

`ash
pytest proyectos/02-simulador-eventos-negocio/tests -q
`

## Límites actuales
- No hay IA (Artificial Intelligence - Inteligencia Artificial) real implementada.
- No hay API (Application Programming Interface - Interfaz de Programación de Aplicaciones) productiva ni llamadas externas.
- No hay datos reales.
- No hay integraciones externas.
- No hay servicios de pago.
- No hay uso de claves.

## Relación con el laboratorio
Este proyecto alimenta escenarios para evaluación operativa de agentes y módulos posteriores del laboratorio orientado a PYME (Small and Medium-sized Enterprise - Pequeña y Mediana Empresa).

##  Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  
(c) 2026 - Txema Ríos. Todos los derechos compartidos.

