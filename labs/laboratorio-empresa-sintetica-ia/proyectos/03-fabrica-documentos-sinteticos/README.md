# 03-fabrica-documentos-sinteticos

## Objetivo
Fábrica de Documentos Sintéticos con alcance V1 (Version 1 - Versión 1) local mínimo. Genera documentos empresariales ficticios reutilizables para pruebas internas del laboratorio.

## Implementado en esta V1 local mínima
- Carga de contexto desde:
  - datos_ejemplo/empresa_sintetica_demo/empresa_sintetica.json
  - datos_ejemplo/eventos_negocio_demo/eventos_negocio.json
- Fallback interno mínimo si los archivos no existen (para pruebas autónomas).
- Generación determinista por seed de tipos documentales mínimos:
  - propuesta_comercial
  - contrato_simulado
  - correo_cliente
  - cta_reunion
  - informe_operativo
  - 	icket_soporte
  - politica_interna
- Exportación en Markdown y JSON (sin PDF ni DOCX):
  - indice_documentos.json
  - esumen_documentos.json
  - documentos .md en carpetas por tipo.
- CLI para configurar seed, entradas, salida y volumen documental.
- Tests con pytest para estructura, reproducibilidad, exportación y límites.

## Cómo ejecutar la demo
Desde la raíz del repositorio:

`ash
python proyectos/03-fabrica-documentos-sinteticos/ejecutar_demo.py --seed 42 --documentos-por-tipo 3
`

Parámetros opcionales:
- --entrada-empresa <ruta_json>
- --entrada-eventos <ruta_json>
- --salida <carpeta>

## Entradas por defecto
- datos_ejemplo/empresa_sintetica_demo/empresa_sintetica.json
- datos_ejemplo/eventos_negocio_demo/eventos_negocio.json

## Salida por defecto
- datos_ejemplo/documentos_sinteticos_demo/
  - indice_documentos.json
  - esumen_documentos.json
  - propuestas_comerciales/*.md
  - contratos_simulados/*.md
  - correos_clientes/*.md
  - ctas_reunion/*.md
  - informes_operativos/*.md
  - 	ickets_soporte/*.md
  - politicas_internas/*.md

## Cómo ejecutar los tests
`ash
pytest proyectos/03-fabrica-documentos-sinteticos/tests -q
`

## Límites actuales
- Los documentos son sintéticos y de uso técnico interno.
- No son documentos reales ni jurídicamente válidos.
- No hay IA (Artificial Intelligence - Inteligencia Artificial) real implementada.
- No hay API (Application Programming Interface - Interfaz de Programación de Aplicaciones) productiva ni llamadas externas.
- No hay datos reales, integraciones externas ni servicios de pago.
- En esta fase no se generan PDF ni DOCX.

##  Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  
(c) 2026 - Txema Ríos. Todos los derechos compartidos.

