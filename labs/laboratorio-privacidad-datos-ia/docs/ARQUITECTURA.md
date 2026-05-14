# Arquitectura V1

Arquitectura local de privacidad de datos para IA con controles técnicos heurísticos y evidencia reproducible.

## Flujo implementado

1. Datos sintéticos con PII ficticia
Carga de `datos/dataset_con_pii_sintetica.json`.
2. Detección
Identificación heurística de PII en entradas y contexto.
3. Anonimización
Transformación de datos sensibles a formato no identificable.
4. Seudonimización
Reemplazo por identificadores seudónimos controlados.
5. Minimización
Reducción del contexto enviado al flujo IA.
6. Validación de salida
Comprobación técnica de posibles fugas de PII.
7. Evaluación de exposición
Cálculo de exposición residual tras transformaciones.
8. Registro de tratamiento
Actualización de `datos/registro_tratamiento_sintetico.json`.
9. Informe final
Generación de `informes/informe_privacidad_datos_ia.md`.

## Componentes

- `privacidad/`: reglas de detección, transformación, validación y evaluación.
- `servicios/`: orquestación y reporte.
- `observabilidad/`: trazas y coste simulado.
- `datos/` e `informes/`: entradas y evidencias.

## Restricciones V1

- Enfoque técnico heurístico, no legal.
- Sin APIs externas ni cloud.
- Sin datos reales.
- Sin certificación de cumplimiento RGPD.

## 🪪 Licencia y Autoría

Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.

© 2025 – Txema Ríos. Todos los derechos compartidos.
