# 01-generador-empresa-sintetica

## Objetivo
Generador de Empresa Sintética con alcance V1 (Version 1 - Versión 1) local mínimo. Produce una empresa ficticia coherente y reproducible para pruebas técnicas sin datos reales.

## Implementado en esta V1 local mínima
- Generación determinista con seed.
- Estructura principal con: empresa, empleados, clientes, productos, procesos, esumen_operativo.
- Exportación a JSON del objeto completo.
- Exportación CSV de empleados, clientes, productos y procesos.
- CLI local para parametrizar volúmenes y carpeta de salida.
- Demo ejecutable en ejecutar_demo.py.
- Pruebas con pytest para estructura, reproducibilidad, cantidades y exportación.

## Estructura técnica
- ejecutar_demo.py
- equirements.txt
- src/generador_empresa_sintetica/
- 	ests/

## Cómo ejecutar la demo
Desde la raíz del repositorio:

`ash
python proyectos/01-generador-empresa-sintetica/ejecutar_demo.py --seed 42 --empleados 12 --clientes 20 --productos 8
`

Salida por defecto:
- datos_ejemplo/empresa_sintetica_demo/

También se puede cambiar con:
- --salida <carpeta>

## Cómo ejecutar tests
Desde la raíz del repositorio:

`ash
pytest proyectos/01-generador-empresa-sintetica/tests -q
`

## Límites actuales
- No hay IA (Artificial Intelligence - Inteligencia Artificial) real implementada.
- No hay API (Application Programming Interface - Interfaz de Programación de Aplicaciones) productiva.
- No hay integraciones externas.
- No hay uso de servicios de pago.
- No hay uso de datos reales.
- No hay gestión de claves.

## Relación con el laboratorio
Este módulo actúa como origen sintético para fases posteriores del laboratorio y para futuros escenarios de evaluación de agentes en una PYME (Small and Medium-sized Enterprise - Pequeña y Mediana Empresa).

##  Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  
(c) 2026 - Txema Ríos. Todos los derechos compartidos.

