# Mapa de Evidencias

Relación entre capacidades declaradas y artefactos reales generados por el laboratorio.

## 1. Informe de gobernanza

- Evidencia principal: `informes/informe_gobernanza_ai_act.md`
- Generación: `python scripts\generar_informe_gobernanza.py`

## 2. Fichas de sistemas IA

- Evidencia principal: `informes/fichas_sistemas_ia/`
- Generación: `python scripts\generar_informe_gobernanza.py`

## 3. Casos de uso IA

- Evidencia: `datos/casos_uso_ia.json`
- Generación/actualización: `python scripts\sembrar_datos.py`

## 4. Matriz de riesgos

- Evidencia: `datos/matriz_riesgos.json`
- Generación/actualización: `python scripts\sembrar_datos.py`

## 5. Obligaciones orientativas

- Evidencia: `datos/obligaciones_orientativas.json`
- Generación/actualización: `python scripts\sembrar_datos.py`

## 6. Evidencias de gobernanza

- Evidencia: `datos/evidencias_gobernanza.json`
- Generación/actualización: `python scripts\sembrar_datos.py`

## 7. Shadow IA sintética

- Evidencia: `datos/shadow_ia_sintetica.json`
- Generación/actualización: `python scripts\sembrar_datos.py`

## 8. Plantillas de soporte

- Política: `plantillas/POLITICA_USO_RESPONSABLE_IA.md`
- Ficha sistema: `plantillas/FICHA_SISTEMA_IA.md`
- Plan alfabetización: `plantillas/PLAN_ALFABETIZACION_IA.md`

## 9. Calidad funcional

- Evidencia: suite `tests/`
- Ejecución: `python -m unittest discover tests -v`

## Alcance V1

No se incluyen evidencias de asesoramiento legal, certificación regulatoria ni análisis normativo automático definitivo porque no forman parte de la implementación.

## 🪪 Licencia y Autoría

Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.

© 2025 – Txema Ríos. Todos los derechos compartidos.
