# Arquitectura V1

Arquitectura local para backend IA simulado con controles de contrato, acceso y operación.

## Flujo implementado

1. Petición sintética
Carga desde `datos/peticiones_backend.json`.
2. Validación de contrato
Comprobación contra `datos/contratos_api.json`.
3. Autenticación ficticia
Verificación de identidad simulada con usuarios/tokens locales.
4. Autorización por rol
Aplicación de permisos por rol y políticas de acceso.
5. Router local
Enrutado interno al módulo IA simulado correspondiente.
6. Módulo IA simulado
Ejecución de respuesta sintética (RAG, privacidad o evaluación).
7. Auditoría
Registro de petición y decisiones de seguridad.
8. Trazabilidad
Seguimiento por `traza_id` y etapas de proceso.
9. Métricas
Cálculo de indicadores locales y costes simulados.
10. Informe
Generación de `informes/informe_backend_ia_empresarial.md`.

## Componentes

- `api/`: contratos, routing y respuesta estructurada.
- `seguridad/`: autenticación/autorización simuladas.
- `colas/`: cola local y jobs.
- `servicios/`: módulos IA simulados y motor backend.
- `auditoria/` y `observabilidad/`: registro, trazas, métricas y costes.

## Restricciones V1

- Sin servidor HTTP productivo ni API pública real.
- Sin framework web obligatorio (sin FastAPI en V1).
- Sin usuarios/credenciales reales.
- Sin integración cloud ni módulos IA externos.

##  Licencia y Autoría

Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.

(c) 2026 - Txema Ríos. Todos los derechos compartidos.

