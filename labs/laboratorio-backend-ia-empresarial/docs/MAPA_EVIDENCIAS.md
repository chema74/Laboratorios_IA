# Mapa de Evidencias

Relación entre capacidades del laboratorio y artefactos reales generados.

## 1. Informe backend

- Evidencia principal: `informes/informe_backend_ia_empresarial.md`
- Generación: `python scripts\ejecutar_demo.py` / `python scripts\ejecutar_backend_local.py`

## 2. Contratos API sintéticos

- Evidencia: `datos/contratos_api.json`
- Generación/actualización: `python scripts\sembrar_datos.py`

## 3. Usuarios y roles sintéticos

- Evidencia: `datos/usuarios_roles.json`
- Generación/actualización: `python scripts\sembrar_datos.py`

## 4. Peticiones backend sintéticas

- Evidencia: `datos/peticiones_backend.json`
- Generación/actualización: `python scripts\sembrar_datos.py`

## 5. Tareas de cola

- Evidencia: `datos/tareas_cola.json`
- Generación/actualización: `python scripts\sembrar_datos.py`

## 6. Módulos IA empresariales simulados

- Evidencia: `datos/modulos_ia_empresarial.json`
- Generación/actualización: `python scripts\sembrar_datos.py`

## 7. Calidad funcional

- Evidencia: suite `tests/`
- Ejecución: `python -m unittest discover tests -v`

## Alcance V1

No se incluyen evidencias de API pública real, credenciales reales o despliegue cloud porque no forman parte de la implementación.

##  Licencia y Autoría

Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.

(c) 2026 - Txema Ríos. Todos los derechos compartidos.

