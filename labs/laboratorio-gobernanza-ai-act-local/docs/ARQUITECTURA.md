# Arquitectura V1

Arquitectura local de gobernanza IA con criterios heurísticos y salida documental orientativa.

## Flujo implementado

1. Casos de uso sintéticos
Carga inicial de `datos/casos_uso_ia.json`.
2. Inventario
Consolidación estructurada de casos de uso IA.
3. Clasificación heurística
Asignación orientativa de nivel de riesgo.
4. Obligaciones orientativas
Cruce con `datos/obligaciones_orientativas.json`.
5. Evidencias
Validación y registro desde `datos/evidencias_gobernanza.json`.
6. Shadow IA
Análisis de usos no formalizados desde `datos/shadow_ia_sintetica.json`.
7. Fichas de sistema
Generación de fichas por caso en `informes/fichas_sistemas_ia/`.
8. Alfabetización
Aplicación de plantilla `plantillas/PLAN_ALFABETIZACION_IA.md`.
9. Política interna
Aplicación de plantilla `plantillas/POLITICA_USO_RESPONSABLE_IA.md`.
10. Informe final
Generación de `informes/informe_gobernanza_ai_act.md`.

## Componentes

- `gobernanza/`: reglas y artefactos de gobernanza.
- `servicios/`: orquestación y reporting.
- `observabilidad/`: trazas y coste simulado.
- `datos/`, `plantillas/`, `informes/`: entradas y evidencias.

## Restricciones V1

- Clasificaciones técnicas y heurísticas, no legales.
- Sin APIs externas ni cloud.
- Sin datos reales.
- Sin certificación de cumplimiento normativo.

## 🪪 Licencia y Autoría

Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.

© 2025 – Txema Ríos. Todos los derechos compartidos.
