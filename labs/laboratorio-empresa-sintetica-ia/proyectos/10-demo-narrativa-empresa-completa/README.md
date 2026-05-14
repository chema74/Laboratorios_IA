# 10-demo-narrativa-empresa-completa

## Objetivo
Construir una demo narrativa local de una semana operativa de empresa ficticia, integrando artefactos de los proyectos 01 a 09.

## Estado actual
V1 (Version 1 – Versión 1) local mínima implementada.

## Qué se ha implementado
- Carga de contexto desde salidas previas del laboratorio (con fallback interno para pruebas).
- Construcción determinista de ficha narrativa, línea temporal semanal, episodios y mapa de evidencias.
- Generación de resumen ejecutivo ficticio, guion de demo y expediente final en Markdown.
- Exportación en JSON y CSV de los artefactos narrativos principales.
- Interfaz CLI local reproducible con `seed`.

## Entradas de referencia (opcionales)
- `datos_ejemplo/empresa_sintetica_demo/empresa_sintetica.json`
- `datos_ejemplo/eventos_negocio_demo/eventos_negocio.json`
- `datos_ejemplo/eventos_negocio_demo/resumen_eventos.json`
- `datos_ejemplo/documentos_sinteticos_demo/indice_documentos.json`
- `datos_ejemplo/documentos_sinteticos_demo/resumen_documentos.json`
- `datos_ejemplo/escenarios_prueba_agentes_demo/escenarios_prueba_agentes.json`
- `datos_ejemplo/escenarios_prueba_agentes_demo/resumen_escenarios.json`
- `datos_ejemplo/crisis_simuladas_demo/crisis_simuladas.json`
- `datos_ejemplo/crisis_simuladas_demo/resumen_crisis.json`
- `datos_ejemplo/revision_humana_demo/revisiones_humanas.json`
- `datos_ejemplo/revision_humana_demo/registro_decisiones.json`
- `datos_ejemplo/revision_humana_demo/resumen_revision_humana.json`
- `datos_ejemplo/gemelo_digital_operativo_demo/estado_operativo.json`
- `datos_ejemplo/gemelo_digital_operativo_demo/alertas_operativas.json`
- `datos_ejemplo/gemelo_digital_operativo_demo/decisiones_simuladas.json`
- `datos_ejemplo/gemelo_digital_operativo_demo/resumen_gemelo_digital.json`
- `datos_ejemplo/privacidad_datos_sinteticos_demo/inventario_datos_sinteticos.json`
- `datos_ejemplo/privacidad_datos_sinteticos_demo/riesgos_privacidad_simulados.json`
- `datos_ejemplo/privacidad_datos_sinteticos_demo/resumen_privacidad_datos_sinteticos.json`
- `datos_ejemplo/comparador_agente_proceso_demo/procesos_comparados.json`
- `datos_ejemplo/comparador_agente_proceso_demo/comparaciones_agente_proceso.json`
- `datos_ejemplo/comparador_agente_proceso_demo/resumen_comparador.json`

## Salida generada
Carpeta por defecto: `datos_ejemplo/demo_narrativa_empresa_completa/`
- `demo_narrativa_empresa_completa.json`
- `linea_tiempo_semanal.json`
- `linea_tiempo_semanal.csv`
- `episodios_narrativos.json`
- `episodios_narrativos.csv`
- `mapa_evidencias.json`
- `mapa_evidencias.csv`
- `resumen_demo_narrativa.json`
- `guion_demo.md`
- `expediente_demo_empresa_completa.md`

## Ejecución de demo
```bash
python proyectos/10-demo-narrativa-empresa-completa/ejecutar_demo.py --seed 42 --dias 7
```

## Ejecución de tests
```bash
pytest proyectos/10-demo-narrativa-empresa-completa/tests -q
```

## Límites explícitos
- No hay IA (Artificial Intelligence – Inteligencia Artificial) real en ejecución.
- No hay API (Application Programming Interface – Interfaz de Programación de Aplicaciones) externa ni productiva.
- No hay datos reales ni cliente real.
- No se ejecutan agentes reales.
- No hay sistema productivo, monitorización real ni recomendación empresarial real.
- No hay servicios de pago.
- Esta demo se orienta a un uso técnico de portfolio para entorno PYME (Small and Medium-sized Enterprise – Pequeña y Mediana Empresa).

## Evolución
- V1: integración narrativa local mínima.
- V2 (Version 2 – Versión 2): evolución futura profesional documentada (fuera de esta implementación).

## 🪪 Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  
© 2025 – Txema Ríos. Todos los derechos compartidos.
