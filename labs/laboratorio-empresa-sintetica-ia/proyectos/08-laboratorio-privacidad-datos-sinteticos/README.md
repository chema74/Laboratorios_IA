# 08-laboratorio-privacidad-datos-sinteticos

## Objetivo
Laboratorio de Privacidad con Datos Sintéticos con alcance V1 (Version 1 – Versión 1) local mínimo. Analiza sensibilidad ficticia, permisos simulados, minimización, anonimización demostrativa y riesgos de exposición sobre artefactos sintéticos del laboratorio.

## Implementado en esta V1 local mínima
- Inspección y carga de artefactos previos (empresa, eventos, documentos, escenarios, crisis, revisiones, estado operativo) desde JSON.
- Fallback interno mínimo para ejecución autónoma y tests.
- Inventario de datos sintéticos con campos de sensibilidad ficticia y señales de minimización/anonimización/revisión humana.
- Clasificación agregada de sensibilidad por origen, entidad, nivel y categoría.
- Matriz de permisos simulados por rol ficticio y tipo de entidad.
- Dataset minimizado con trazabilidad de campos eliminados o resumidos.
- Dataset anonimizado de demostración determinista con seed.
- Riesgos de privacidad simulados con severidad, estado y recomendación prudente.
- Exportación completa en JSON/CSV + expediente Markdown.

## Cómo ejecutar la demo
Desde la raíz del repositorio:

`ash
python proyectos/08-laboratorio-privacidad-datos-sinteticos/ejecutar_demo.py --seed 42 --max-datos 80
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

## Salida por defecto
- datos_ejemplo/privacidad_datos_sinteticos_demo/
  - inventario_datos_sinteticos.json
  - inventario_datos_sinteticos.csv
  - clasificacion_sensibilidad.json
  - clasificacion_sensibilidad.csv
  - matriz_permisos_simulados.json
  - matriz_permisos_simulados.csv
  - dataset_minimizado_demo.json
  - dataset_anonimizado_demo.json
  - iesgos_privacidad_simulados.json
  - iesgos_privacidad_simulados.csv
  - esumen_privacidad_datos_sinteticos.json
  - expediente_privacidad_datos_sinteticos.md

## Cómo ejecutar los tests
`ash
pytest proyectos/08-laboratorio-privacidad-datos-sinteticos/tests -q
`

## Límites actuales
- Datos y resultados estrictamente sintéticos.
- No hay datos reales.
- No hay auditoría legal real.
- No hay cumplimiento real.
- No hay anonimización certificada.
- No se ejecutan agentes reales.
- No hay IA (Artificial Intelligence – Inteligencia Artificial) real implementada.
- No hay API (Application Programming Interface – Interfaz de Programación de Aplicaciones) productiva ni llamadas externas.
- No hay integraciones externas ni servicios de pago.

## Propósito de esta base
Este proyecto prepara la base para seguridad defensiva, evaluación de agentes, gobierno de datos y futuras demos empresariales.

## 🪪 Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  
© 2025 – Txema Ríos. Todos los derechos compartidos.
