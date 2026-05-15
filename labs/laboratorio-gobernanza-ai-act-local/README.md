# laboratorio-gobernanza-ai-act-local

Laboratorio **local, gratuito y reproducible** para gobernanza de IA en entorno empresarial, alineado de forma orientativa con principios del AI Act. Esta V1 organiza inventario, riesgos heurísticos, obligaciones orientativas y evidencias internas sin pretensión de dictamen legal.

> Este repositorio **no constituye asesoramiento legal**. Las clasificaciones y resultados son técnicos, heurísticos y orientativos.

## Problema empresarial que simula

Simula una organización que necesita ordenar usos de IA, clasificar riesgo de forma orientativa, detectar shadow IA, generar evidencias y preparar documentación interna de gobernanza antes de escalar iniciativas.

## Capacidades implementadas en V1

- Inventario de casos de uso IA.
- Clasificación heurística de riesgo.
- Matriz de obligaciones orientativas.
- Registro de evidencias.
- Análisis de shadow IA.
- Generación de fichas de sistema IA.
- Plan de alfabetización IA.
- Política de uso responsable.
- Informe Markdown de gobernanza.

## Límites explícitos de la V1

- No es asesoramiento legal.
- No sustituye revisión jurídica.
- No certifica cumplimiento normativo.
- No usa datos reales.
- No usa servicios cloud.
- No ejecuta análisis legal automático definitivo.
- No es una herramienta de compliance cerrada ni productiva.

## Ejecución rápida (Windows PowerShell)

```powershell
python scripts\sembrar_datos.py
python scripts\comprobar_salud.py
python scripts\ejecutar_demo.py
python scripts\generar_informe_gobernanza.py
python -m unittest discover tests -v
```

## Evidencias principales

- Informe de gobernanza: `informes\informe_gobernanza_ai_act.md`.
- Fichas de sistema: `informes\fichas_sistemas_ia\`.
- Datos sintéticos: `datos\casos_uso_ia.json`, `datos\matriz_riesgos.json`, `datos\obligaciones_orientativas.json`, `datos\evidencias_gobernanza.json`, `datos\shadow_ia_sintetica.json`.
- Plantillas de soporte: `plantillas\POLITICA_USO_RESPONSABLE_IA.md`, `plantillas\FICHA_SISTEMA_IA.md`, `plantillas\PLAN_ALFABETIZACION_IA.md`.
- Validación funcional: suite `tests\`.

## Documentación principal

- Catálogo: [CATALOGO.md](CATALOGO.md)
- Arquitectura: [docs/ARQUITECTURA.md](docs/ARQUITECTURA.md)
- Guía de ejecución: [docs/GUIA_EJECUCION.md](docs/GUIA_EJECUCION.md)
- Decisiones técnicas: [docs/DECISIONES_TECNICAS.md](docs/DECISIONES_TECNICAS.md)
- Mapa de evidencias: [docs/MAPA_EVIDENCIAS.md](docs/MAPA_EVIDENCIAS.md)
- Límites legales y supuestos: [docs/LIMITES_LEGALES_Y_SUPUESTOS.md](docs/LIMITES_LEGALES_Y_SUPUESTOS.md)

##  Licencia y Autoría

Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.

(c) 2026 - Txema Ríos. Todos los derechos compartidos.

