# Catálogo V1

Catálogo de módulos del laboratorio backend y evidencia que produce cada bloque.

## Aplicación

- `app/main.py`: entrada CLI para ejecutar demo, backend local y cola.
Evidencia: ejecución reproducible de flujos principales.
- `app/config.py`: configuración de rutas y parámetros.
Evidencia: resolución consistente de datos e informe.
- `app/modelos.py`: estructuras de petición, respuesta y eventos.
Evidencia: intercambio tipado entre seguridad, router, auditoría y servicios.

## API local simulada

- `api/validacion_contratos.py`: validación de contratos API sintéticos.
Evidencia: comprobación de campos y estructura de peticiones.
- `api/router_local.py`: enrutado local hacia módulos IA simulados.
Evidencia: selección de módulo por endpoint interno.
- `api/respuestas.py`: respuestas estructuradas del flujo.
Evidencia: salida uniforme para demo e informe.

## Seguridad simulada

- `seguridad/autenticacion_ficticia.py`: autenticación con tokens ficticios.
Evidencia: aceptación/rechazo técnico de identidad simulada.
- `seguridad/autorizacion_roles.py`: control por rol sobre endpoints.
Evidencia: decisiones de acceso por usuario/rol sintético.
- `seguridad/politicas_acceso.py`: reglas de acceso locales.
Evidencia: políticas aplicadas en validación de petición.

## Cola y jobs

- `colas/cola_simulada.py`: almacenamiento en cola local.
Evidencia: tareas pendientes y estado de procesamiento.
- `colas/jobs_locales.py`: definición de jobs deterministas.
Evidencia: ejecución controlada de trabajo en segundo plano simulado.
- `colas/procesador_tareas.py`: consumo y procesamiento de cola.
Evidencia: avance de tareas registradas.

## Servicios IA simulados

- `servicios/modulo_rag_simulado.py`: simulación de módulo RAG.
- `servicios/modulo_privacidad_simulado.py`: simulación de módulo de privacidad.
- `servicios/modulo_evaluacion_simulado.py`: simulación de evaluación.
Evidencia: respuestas sintéticas por módulo.
- `servicios/motor_backend.py`: orquestación backend extremo a extremo.
Evidencia: flujo consolidado de validación, seguridad, routing y auditoría.
- `servicios/generador_informes.py`: generación de informe Markdown.
Evidencia: `informes/informe_backend_ia_empresarial.md`.

## Auditoría y observabilidad

- `auditoria/registro_peticiones.py`: registro de peticiones.
Evidencia: rastro de operación por transacción.
- `auditoria/trazabilidad.py`: trazabilidad de decisiones y etapas.
Evidencia: seguimiento de flujo por `traza_id`.
- `observabilidad/metricas.py`: métricas locales de operación.
Evidencia: indicadores agregados de backend simulado.
- `observabilidad/costes_simulados.py`: cálculo de coste simulado.
Evidencia: coste operativo ficticio por ejecución.

## Datos, scripts y pruebas

- Datos: `datos/contratos_api.json`, `datos/usuarios_roles.json`, `datos/peticiones_backend.json`, `datos/tareas_cola.json`, `datos/modulos_ia_empresarial.json`.
- Scripts: `scripts/sembrar_datos.py`, `scripts/comprobar_salud.py`, `scripts/ejecutar_demo.py`, `scripts/ejecutar_backend_local.py`, `scripts/procesar_cola.py`.
- Pruebas: `tests/`.

## 🪪 Licencia y Autoría

Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.

© 2025 – Txema Ríos. Todos los derechos compartidos.
