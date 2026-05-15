# laboratorio-backend-ia-empresarial

Laboratorio **local, gratuito y reproducible** para simular una capa backend empresarial que integra módulos de IA con control operativo. Esta V1 prioriza contratos, seguridad ficticia, auditoría y trazabilidad en entorno offline, sin pretensión productiva.

## Problema empresarial que simula

Simula cómo integrar módulos IA en una capa backend controlada, auditable y operable, antes de considerar un despliegue real con servicios y seguridad de producción.

## Capacidades implementadas en V1

- Contratos API sintéticos.
- Router local simulado.
- Autenticación ficticia.
- Autorización por roles.
- Políticas de acceso.
- Cola simulada.
- Jobs locales.
- Módulos IA simulados.
- Auditoría de peticiones.
- Trazabilidad.
- Métricas locales.
- Costes simulados.
- Informe Markdown.

## Límites explícitos de la V1

- Sin servidor HTTP productivo obligatorio.
- Sin FastAPI en V1.
- Sin usuarios reales.
- Sin credenciales reales.
- Sin módulos IA externos.
- Sin cloud.
- Sin uso productivo.

## Ejecución rápida (Windows PowerShell)

```powershell
python scripts\sembrar_datos.py
python scripts\comprobar_salud.py
python scripts\ejecutar_demo.py
python scripts\ejecutar_backend_local.py
python scripts\procesar_cola.py
python -m unittest discover tests -v
```

## Evidencias principales

- Informe: `informes\informe_backend_ia_empresarial.md`.
- Datos base: `datos\contratos_api.json`, `datos\usuarios_roles.json`, `datos\peticiones_backend.json`, `datos\tareas_cola.json`, `datos\modulos_ia_empresarial.json`.
- Validación funcional: suite `tests\`.

## Documentación principal

- Catálogo: [CATALOGO.md](CATALOGO.md)
- Arquitectura: [docs/ARQUITECTURA.md](docs/ARQUITECTURA.md)
- Guía de ejecución: [docs/GUIA_EJECUCION.md](docs/GUIA_EJECUCION.md)
- Decisiones técnicas: [docs/DECISIONES_TECNICAS.md](docs/DECISIONES_TECNICAS.md)
- Mapa de evidencias: [docs/MAPA_EVIDENCIAS.md](docs/MAPA_EVIDENCIAS.md)
- Contratos API: [docs/CONTRATOS_API.md](docs/CONTRATOS_API.md)

##  Licencia y Autoría

Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.

(c) 2026 - Txema Ríos. Todos los derechos compartidos.

