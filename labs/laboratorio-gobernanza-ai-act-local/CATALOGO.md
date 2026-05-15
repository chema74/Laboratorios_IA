# Catálogo V1

Catálogo de módulos de gobernanza IA con evidencia asociada para revisión técnica de portfolio.

## Aplicación

- `app/main.py`: entrada CLI del laboratorio.
Evidencia: ejecución local de demo e informe.
- `app/config.py`: configuración de rutas y parámetros.
Evidencia: consistencia de acceso a datos, plantillas e informes.
- `app/modelos.py`: estructuras de datos del dominio de gobernanza.
Evidencia: interoperabilidad entre motor, reglas y reporting.

## Núcleo de gobernanza

- `gobernanza/inventario_casos_uso.py`: inventario de casos de uso IA.
Evidencia: consolidación de casos desde `datos/casos_uso_ia.json`.
- `gobernanza/clasificador_riesgo.py`: clasificación heurística de riesgo.
Evidencia: asignación orientativa de nivel de riesgo.
- `gobernanza/matriz_obligaciones.py`: mapeo de obligaciones orientativas.
Evidencia: relación riesgo-obligaciones en informe final.
- `gobernanza/registro_evidencias.py`: control de evidencias documentales.
Evidencia: validación/registro desde `datos/evidencias_gobernanza.json`.
- `gobernanza/shadow_ia.py`: análisis de shadow IA sintética.
Evidencia: detección de usos no formalizados en `datos/shadow_ia_sintetica.json`.
- `gobernanza/ficha_sistema_ia.py`: generación de fichas por sistema.
Evidencia: archivos en `informes/fichas_sistemas_ia/`.
- `gobernanza/alfabetizacion_ia.py`: preparación de plan de alfabetización.
Evidencia: uso de plantilla `plantillas/PLAN_ALFABETIZACION_IA.md`.
- `gobernanza/politica_uso_responsable.py`: política interna de uso responsable.
Evidencia: uso de plantilla `plantillas/POLITICA_USO_RESPONSABLE_IA.md`.

## Servicios

- `servicios/motor_gobernanza.py`: orquestación del flujo de gobernanza.
Evidencia: cálculo integrado de salida documental.
- `servicios/generador_informes.py`: generación de informes Markdown.
Evidencia: `informes/informe_gobernanza_ai_act.md` y fichas de sistema.

## Observabilidad

- `observabilidad/trazas.py`: trazabilidad de ejecución.
Evidencia: registro técnico de etapas ejecutadas.
- `observabilidad/costes_simulados.py`: coste simulado de operación.
Evidencia: estimación local de coste de proceso.

## Datos, plantillas y salidas

- Datos: `datos/casos_uso_ia.json`, `datos/matriz_riesgos.json`, `datos/obligaciones_orientativas.json`, `datos/evidencias_gobernanza.json`, `datos/shadow_ia_sintetica.json`.
- Plantillas: `plantillas/FICHA_SISTEMA_IA.md`, `plantillas/PLAN_ALFABETIZACION_IA.md`, `plantillas/POLITICA_USO_RESPONSABLE_IA.md`.
- Salidas: `informes/informe_gobernanza_ai_act.md`, `informes/fichas_sistemas_ia/`.

## Scripts y pruebas

- `scripts/sembrar_datos.py`: preparación de datos sintéticos.
- `scripts/comprobar_salud.py`: chequeo de integridad operativa.
- `scripts/ejecutar_demo.py`: ejecución demo del laboratorio.
- `scripts/generar_informe_gobernanza.py`: informe completo de gobernanza.
- `tests/`: pruebas unitarias de clasificación, inventario, evidencias, shadow IA y motor.

##  Licencia y Autoría

Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.

(c) 2026 - Txema Ríos. Todos los derechos compartidos.

