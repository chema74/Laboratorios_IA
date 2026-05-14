# Informe de Evaluación LLM Local V1

## Resumen ejecutivo
- Total respuestas evaluadas: 7
- Media puntuación total: 0.7892
- Casos con riesgo de alucinación: 1
- Coste simulado total: 0.00839 EUR

## Casos aprobados
- CASO-001 / R-001-A -> 0.8667
- CASO-002 / R-002-A -> 0.8889
- CASO-003 / R-003-A -> 0.85
- CASO-004 / R-004-A -> 0.7752
- CASO-005 / R-005-A -> 0.8381
- CASO-006 / R-006-A -> 0.9444

## Casos con riesgo
- CASO-001 / R-001-B -> alertas=["Cifras/fechas no respaldadas: ['12']", 'Afirmación absoluta potencialmente no respaldada']

## Regresiones detectadas
- CASO-002: empeora (delta=-2)
- CASO-004: estable (delta=0)

## Recomendaciones técnicas
- Reforzar prompts en casos con cobertura parcial de criterios clave.
- Evitar cifras no respaldadas por la referencia esperada.
- Exigir trazabilidad explícita en formato 'según política/procedimiento'.