#  GUÍA DE REVISIÓN EJECUTIVA DE EVIDENCIAS V2 - LABORATORIO EVALUACIÓN LLM LOCAL

## Documento de apoyo para evaluación profesional

---

## 1. Objetivo

Esta guía explica cómo revisar las evidencias generadas por la V2 (Version 2 - Versión 2) del repositorio `laboratorio-evaluacion-llm-local`.

Su finalidad es ayudar a una empresa, consultor TIC (Information and Communication Technologies - Tecnologías de la Información y la Comunicación) o evaluador técnico a entender qué demuestra el laboratorio y qué no debe interpretarse como sistema productivo.

---

## 2. Principio de lectura

Las evidencias deben leerse como señales de madurez técnica local, no como promesa de evaluación empresarial completa.

Este laboratorio demuestra una base reproducible y documentada para revisar criterios de calidad en LLM (Large Language Model - Gran Modelo de Lenguaje).

No debe presentarse como SaaS (Software as a Service - Software como Servicio), plataforma cerrada ni benchmark industrial definitivo.

---

## 3. Evidencias principales

Las evidencias V2 más importantes son:

- `scripts/validar_v2.py`
- `salidas/validacion_v2_evaluacion_llm.md`
- `scripts/generar_informe_ejecutivo_v2.py`
- `salidas/informe_ejecutivo_v2_evaluacion_llm.md`
- `docs/PLAN_V2_LABORATORIO_EVALUACION_LLM.md`
- `docs/MAPA_EVIDENCIAS_V2.md`
- `docs/LIMITES_ALCANCE_V2.md`
- Tests automatizados del repositorio.

Las salidas de `salidas/` son evidencias generadas localmente y no forman parte del código fuente versionado.

---

## 4. Cómo revisar la validación V2

Debe revisarse:

- Que los documentos V2 existen.
- Que hay documentación base en `docs/`.
- Que existen scripts locales.
- Que existen tests automatizados.
- Que los documentos V2 contienen licencia y autoría.
- Que no aparecen patrones visibles de mojibake UTF-8.
- Que la web pública `chema74.github.io` no ha sido modificada.
- Que la rama `main` no ha sido modificada.

---

## 5. Cómo revisar el informe ejecutivo V2

El informe ejecutivo V2 debe responder:

- Qué documentación existe.
- Qué scripts están disponibles.
- Qué evidencias locales se han generado.
- Qué resultado de validación se detecta.
- Qué valor profesional representa el laboratorio.
- Qué límites reconoce.

El informe ejecutivo debe ordenar el proyecto, no exagerarlo.

---

## 6. Señales positivas

Se consideran señales positivas:

- Repositorio ejecutable localmente.
- Validación V2 reproducible.
- Informe ejecutivo generado por script.
- Documentación de límites explícita.
- Sin APIs de pago obligatorias.
- Sin claves reales.
- Sin modificación de la web pública.
- Sin modificación de `main`.
- Rama V2 separada y trazable.

---

## 7. Señales de riesgo

Deben revisarse con cuidado:

- Afirmaciones de benchmark definitivo.
- Promesas de evaluación productiva sin despliegue real.
- Falta de ground truth.
- Métricas poco explicadas.
- Confusión entre puntuación automática y calidad real.
- Documentación que prometa más de lo que el código demuestra.

---

## 8. Estado de esta guía

Esta guía no modifica el comportamiento del repositorio.

No añade dependencias.

No toca `main`.

No toca la web pública.

Su función es mejorar la revisión profesional de las evidencias V2.

---

##  Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.
(c) 2026 - Txema Ríos. Todos los derechos compartidos.
