# Ficha de Portfolio

## Título del proyecto
Laboratorio Empresa Sintética IA

## Subtítulo
V1 local integradora para generación y simulación de una empresa sintética completa, orientada a validación técnica reproducible.

## Descripción breve
Repositorio técnico que reúne 10 módulos locales para construir una narrativa operativa de empresa sintética: generación de datos base, simulación de eventos, creación de documentos, escenarios de prueba, crisis, revisión humana, privacidad, comparativa agente/proceso y demo final consolidada.

## Problema que resuelve
Permite practicar diseño, orquestación y validación de flujos empresariales sintéticos sin depender de datos reales, claves, servicios de pago ni integraciones externas obligatorias. Reduce fricción para experimentar de forma controlada y trazable en entorno local.

## Qué demuestra técnicamente
- Diseño modular de un laboratorio multi-proyecto.
- Trazabilidad de artefactos sintéticos por etapas funcionales.
- Validación automática del conjunto mediante suite de tests.
- Reproducibilidad local con ejecución por scripts y parámetros.
- Capacidad de integrar resultados parciales en una demo narrativa final.

## Arquitectura funcional resumida
1. Generación base de entidad y contexto empresarial sintético.
2. Simulación de actividad operativa (eventos, documentos, escenarios, crisis).
3. Evaluación complementaria (revisión humana simulada, privacidad, comparativa de enfoque).
4. Integración final en narrativa ejecutable de punta a punta.

## Módulos internos (10)
1. `01-generador-empresa-sintetica`
2. `02-simulador-eventos-negocio`
3. `03-fabrica-documentos-sinteticos`
4. `04-generador-escenarios-prueba-agentes`
5. `05-motor-simulacion-crisis`
6. `06-simulador-revision-humana`
7. `07-gemelo-digital-operativo-ligero`
8. `08-laboratorio-privacidad-datos-sinteticos`
9. `09-comparador-agente-proceso`
10. `10-demo-narrativa-empresa-completa`

## Evidencias generadas
- `datos_ejemplo/empresa_sintetica_demo`
- `datos_ejemplo/eventos_negocio_demo`
- `datos_ejemplo/documentos_sinteticos_demo`
- `datos_ejemplo/escenarios_prueba_agentes_demo`
- `datos_ejemplo/crisis_simuladas_demo`
- `datos_ejemplo/revision_humana_demo`
- `datos_ejemplo/gemelo_digital_operativo_demo`
- `datos_ejemplo/privacidad_datos_sinteticos_demo`
- `datos_ejemplo/comparador_agente_proceso_demo`
- `datos_ejemplo/demo_narrativa_empresa_completa`

## Comandos principales de validación
Desde la raíz del repositorio:

```powershell
python -m pytest .\proyectos -q
python .\proyectos\10-demo-narrativa-empresa-completa\ejecutar_demo.py --seed 42 --dias 7
```

## Límites honestos
- No utiliza datos reales ni opera con cliente real.
- No ejecuta IA funcional real en producción.
- No expone API productiva.
- No incluye dashboard productivo.
- No integra de forma real Google Workspace ni Microsoft 365.
- No realiza auditoría legal real.
- No realiza predicción empresarial real.
- No constituye benchmark real de rendimiento empresarial.
- No entrega recomendación empresarial real.
- No es un sistema productivo final.

## Por qué es relevante para empresas
Es relevante como entorno de laboratorio para prototipado técnico, evaluación metodológica y comunicación de arquitectura en iniciativas de automatización o analítica, antes de pasar a fases con datos reales, gobierno formal y operación productiva.

## Posibles evoluciones V2 futuras
- API local con FastAPI para orquestación de ejecuciones.
- Dashboard local (HTML o Streamlit) para navegación de resultados.
- Persistencia analítica con DuckDB y Parquet.
- Exportación estructurada de paquete de evidencias.
- Integraciones opcionales con APIs gratuitas mediante `.env`.
- Extensiones documentadas para conectores de Google o Microsoft sin dependencia obligatoria.

## Estado actual del repositorio
- V1 local integradora completada.
- 10 proyectos internos implementados.
- 70 tests pasando.
- Demo narrativa final disponible.
- Funcionamiento local.
- Sin datos reales.
- Sin APIs externas obligatorias.
- Sin claves.
- Sin servicios de pago.
- Sin IA real ejecutándose todavía.
- Sin sistema productivo.

## 🪪 Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  
© 2025 – Txema Ríos. Todos los derechos compartidos.
