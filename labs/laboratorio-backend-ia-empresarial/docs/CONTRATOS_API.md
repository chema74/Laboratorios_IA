# Contratos API Locales (V1)

Los contratos de esta V1 son **locales y sintéticos**. Se usan para validar la forma de peticiones simuladas en un backend offline.

## Campos mínimos validados

- `endpoint`: ruta lógica local a resolver por router interno.
- `metodo`: operación declarada (por ejemplo `GET`/`POST` simulado).
- `payload`: contenido de entrada de la petición.
- `usuario`: identidad sintética solicitante.
- `rol`: rol sintético aplicado para autorización.
- `traza_id`: identificador de trazabilidad por transacción.

## Cómo se simula una petición

1. Se toma un registro de `datos/peticiones_backend.json`.
2. Se valida estructura y campos contra `datos/contratos_api.json`.
3. Se aplica autenticación ficticia y autorización por rol.
4. El router local deriva la petición a un módulo IA simulado.
5. Se registra auditoría y trazabilidad de resultado.

## Límites de esta V1

- No hay API pública real.
- No hay seguridad productiva.
- No hay autenticación real.
- No hay servidor HTTP de producción.

## 🪪 Licencia y Autoría

Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.

© 2025 – Txema Ríos. Todos los derechos compartidos.
