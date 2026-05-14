# 🧪 GUÍA DE REVISIÓN EJECUTIVA DE EVIDENCIAS V2 — LABORATORIO RAG CORPORATIVO LOCAL

## Documento de apoyo para evaluación profesional

---

## 1. Objetivo

Esta guía explica cómo revisar las evidencias generadas por la V2 (Version 2 – Versión 2) del repositorio `laboratorio-rag-corporativo-local`.

Su finalidad es ayudar a una empresa, consultor TIC (Information and Communication Technologies – Tecnologías de la Información y la Comunicación) o evaluador técnico a entender qué demuestra el laboratorio y qué no debe interpretarse como producto final.

El laboratorio se centra en RAG (Retrieval-Augmented Generation – Generación Aumentada por Recuperación) corporativo local: recuperación documental, trazabilidad, validación y lectura profesional de evidencias.

---

## 2. Principio de lectura

Las evidencias deben leerse como señales de madurez técnica local, no como promesa de despliegue productivo.

Este laboratorio demuestra una base reproducible y documentada para trabajar con documentación corporativa mediante recuperación de contexto.

No debe presentarse como SaaS (Software as a Service – Software como Servicio), plataforma cerrada ni sistema listo para producción.

---

## 3. Evidencias principales

Las evidencias V2 más importantes son:

- `scripts/validar_v2.py`
- `salidas/validacion_v2_rag.md`
- `scripts/generar_informe_ejecutivo_v2.py`
- `salidas/informe_ejecutivo_v2_rag.md`
- `docs/PLAN_V2_LABORATORIO_RAG.md`
- `docs/MAPA_EVIDENCIAS_V2.md`
- `docs/LIMITES_ALCANCE_V2.md`
- Tests automatizados del repositorio.

Las salidas de `salidas/` son evidencias generadas localmente y no forman parte del código fuente versionado.

---

## 4. Cómo revisar la validación V2

La validación V2 permite comprobar que la estructura mínima del laboratorio sigue siendo coherente.

Debe revisarse:

- Que los documentos V2 existen.
- Que los documentos base existen.
- Que los scripts base existen.
- Que los tests base existen.
- Que los documentos V2 contienen licencia y autoría.
- Que no aparecen patrones visibles de mojibake UTF-8 (Unicode Transformation Format 8-bit – Formato de Transformación Unicode de 8 bits).
- Que la web pública `chema74.github.io` no ha sido modificada.
- Que la rama `main` no ha sido modificada.

Una validación correcta no convierte el laboratorio en producto final. Indica que la base técnica local está controlada.

---

## 5. Cómo revisar el informe ejecutivo V2

El informe ejecutivo V2 debe permitir una lectura rápida del estado del laboratorio.

Debe responder:

- Qué documentación clave existe.
- Qué scripts están disponibles.
- Qué evidencias locales se han generado.
- Qué resultado de validación se detecta.
- Qué valor empresarial representa el laboratorio.
- Qué límites reconoce.

El informe ejecutivo debe ordenar el proyecto, no adornarlo.

---

## 6. Cómo revisar los tests

Los tests deben interpretarse como una evidencia mínima de control técnico.

Debe comprobarse:

- Que `python -m pytest -q` pasa correctamente.
- Que los tests no dependen de claves reales.
- Que los tests no requieren servicios cloud obligatorios.
- Que las pruebas añadidas para V2 validan funciones concretas del validador y del informe ejecutivo.

Los tests actuales no sustituyen una evaluación masiva de calidad RAG, pero sí demuestran disciplina básica de ingeniería.

---

## 7. Señales positivas

Se consideran señales positivas:

- Repositorio ejecutable localmente.
- Validación V2 reproducible.
- Informe ejecutivo generado por script.
- Documentación de límites explícita.
- Separación entre laboratorio y producto.
- Sin APIs (Application Programming Interfaces – Interfaces de Programación de Aplicaciones) de pago obligatorias.
- Sin claves reales.
- Sin modificación de la web pública.
- Sin modificación de `main`.
- Rama V2 separada y trazable.

---

## 8. Señales de riesgo

Deben revisarse con cuidado:

- Afirmaciones de producción sin despliegue real.
- Promesas de seguridad corporativa avanzada no implementada.
- Uso de datos sensibles reales.
- Falta de control de permisos por usuario.
- Evaluación insuficiente de calidad de recuperación.
- Confusión entre demo local y producto comercial.
- Dependencia oculta de modelos cloud.
- Documentación que prometa más de lo que el código demuestra.

---

## 9. Lectura empresarial

El laboratorio puede explicarse como una base para conversaciones sobre:

- Consulta documental interna.
- Recuperación de conocimiento corporativo.
- Reducción de búsqueda manual.
- Diseño de pilotos RAG internos.
- Evaluación de trazabilidad documental.
- Gobernanza inicial de sistemas de IA (Artificial Intelligence – Inteligencia Artificial) aplicados a documentación.

Su fortaleza está en ser comprensible, local y verificable.

---

## 10. Estado de esta guía

Esta guía no modifica el comportamiento del repositorio.

No añade dependencias.

No toca `main`.

No toca la web pública.

Su función es mejorar la revisión profesional de las evidencias V2.

---

## 🪪 Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.
© 2025 – Txema Ríos. Todos los derechos compartidos.