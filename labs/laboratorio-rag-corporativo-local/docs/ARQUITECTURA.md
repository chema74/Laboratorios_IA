# Arquitectura V1

Arquitectura local por CLI, orientada a reproducibilidad y trazabilidad documental en entorno corporativo simulado.

## Flujo implementado

1. Datos sintéticos
Carga del corpus en `datos/brutos/documentos_corporativos.json`.
2. Segmentación
Partición de documentos en fragmentos trazables para recuperación.
3. Recuperación
Búsqueda híbrida local con señal léxica y metadatos de negocio.
4. Reordenación
Ajuste final del ranking para priorizar fragmentos más útiles.
5. Generación extractiva
Respuesta basada en extracción, con citas obligatorias a fragmentos recuperados.
6. Seguridad
Guardia de entrada y filtro de salida para evitar consultas/salidas no conformes.
7. Evaluación
Medición offline contra dataset dorado en `evaluacion/dataset_dorado.json`.
8. Observabilidad
Registro de trazas de etapa y coste simulado por consulta.

## Componentes y responsabilidades

- `app/`: entrada y configuración de ejecución local.
- `componentes/`: segmentación, recuperación y reordenación.
- `servicios/`: orquestación del pipeline y generación de respuesta.
- `seguridad/`: validaciones de entrada y control de salida.
- `observabilidad/`: trazas y coste simulado.
- `evaluacion/`: dataset dorado, runner e informes.

## Restricciones explícitas de diseño

- Sin dependencias de cloud.
- Sin APIs externas.
- Sin LLM externo.
- Sin embeddings externos.
- Sin vector database real.
- Sin datos reales de empresa.

Estas restricciones son intencionales para mantener coste cero operativo, ejecución local y revisión técnica reproducible.

##  Licencia y Autoría

Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.

(c) 2026 - Txema Ríos. Todos los derechos compartidos.

