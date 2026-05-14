# Catálogo V1

Catálogo de módulos del laboratorio de privacidad y evidencia generada por cada bloque.

## Aplicación

- `app/main.py`: entrada CLI del flujo de privacidad.
Evidencia: ejecución local reproducible de demo e informe.
- `app/config.py`: configuración de rutas y parámetros.
Evidencia: resolución coherente de datos y salidas.
- `app/modelos.py`: estructuras de datos de casos, transformaciones y resultados.
Evidencia: intercambio consistente entre módulos de privacidad y motor.

## Núcleo de privacidad

- `privacidad/detector_pii.py`: detección heurística de PII sintética.
Evidencia: marcas de coincidencias sobre dataset de entrada.
- `privacidad/anonimizador.py`: anonimización de campos sensibles.
Evidencia: reemplazos irreversibles en artefactos de salida.
- `privacidad/seudonimizador.py`: seudonimización con identificadores controlados.
Evidencia: tokens seudónimos trazables dentro del entorno sintético.
- `privacidad/minimizador_contexto.py`: reducción de contexto no necesario.
Evidencia: prompts minimizados para menor exposición.
- `privacidad/validador_salida.py`: validación de salidas frente a fugas de PII.
Evidencia: alertas/estado de cumplimiento técnico de salida.
- `privacidad/evaluador_exposicion.py`: evaluación de exposición residual.
Evidencia: nivel de riesgo técnico reportado.
- `privacidad/registro_tratamiento.py`: registro sintético de tratamiento de datos.
Evidencia: consolidación en `datos/registro_tratamiento_sintetico.json`.
- `privacidad/politicas_retencion.py`: reglas de retención sintéticas.
Evidencia: uso de `datos/politicas_privacidad_sinteticas.json`.

## Servicios

- `servicios/motor_privacidad.py`: orquestación del pipeline completo.
Evidencia: resultados integrados de detección, transformación y validación.
- `servicios/generador_informes.py`: generación de informe Markdown.
Evidencia: `informes/informe_privacidad_datos_ia.md`.

## Observabilidad

- `observabilidad/trazas.py`: trazabilidad por etapas.
Evidencia: seguimiento técnico del flujo ejecutado.
- `observabilidad/costes_simulados.py`: coste simulado de operación.
Evidencia: estimación local sin proveedores externos.

## Datos y salidas

- `datos/dataset_con_pii_sintetica.json`: dataset base con PII ficticia.
- `datos/prompts_con_contexto_sensible.json`: prompts con contexto sensible sintético.
- `datos/salidas_ia_sinteticas.json`: salidas candidatas para validación.
- `datos/registro_tratamiento_sintetico.json`: registro sintético de tratamiento.
- `datos/politicas_privacidad_sinteticas.json`: reglas sintéticas de retención y manejo.
- `informes/informe_privacidad_datos_ia.md`: evidencia consolidada de evaluación.

## Scripts y pruebas

- `scripts/sembrar_datos.py`: siembra de datos sintéticos.
- `scripts/comprobar_salud.py`: verificación de integridad operativa.
- `scripts/ejecutar_demo.py`: ejecución demostrativa.
- `scripts/generar_informe_privacidad.py`: emisión de informe final.
- `tests/`: validación unitaria de detector, transformadores, validador y motor.

## 🪪 Licencia y Autoría

Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.

© 2025 – Txema Ríos. Todos los derechos compartidos.
