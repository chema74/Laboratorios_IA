"""Generador de guion Markdown para presentar la demo en portfolio."""

from __future__ import annotations


def construir_guion_demo(narrativa: dict) -> str:
    ficha = narrativa["ficha_narrativa_empresa"]
    resumen = narrativa["resumen_ejecutivo_ficticio"]

    return f"""# Guion de Demo - Empresa Completa Sintética

## Apertura
Esta demo presenta una semana operativa completamente sintética para la empresa `{ficha['nombre_empresa']}`.

## Problema que resuelve
Permite mostrar evaluación técnica y trazabilidad de IA empresarial sin exponer datos reales ni usar servicios externos.

## Recorrido por proyectos 01 a 10
1. Proyecto 01: genera la empresa sintética base.
2. Proyecto 02: simula eventos operativos.
3. Proyecto 03: fabrica documentos sintéticos.
4. Proyecto 04: crea escenarios de prueba para agentes simulados.
5. Proyecto 05: introduce crisis sintéticas controladas.
6. Proyecto 06: agrega revisión humana simulada y trazabilidad.
7. Proyecto 07: consolida estado operativo del gemelo digital ligero.
8. Proyecto 08: clasifica sensibilidad y riesgos de privacidad simulados.
9. Proyecto 09: compara flujo manual, automatizado clásico y asistido por agente simulado.
10. Proyecto 10: integra todos los artefactos en una narrativa semanal.

## Demo de datos generados
Mostrar empresa sintética, eventos, documentos y resúmenes agregados.

## Demo de eventos
Explicar pagos pendientes, retrasos y alertas sintéticas de negocio.

## Demo de documentos
Enseñar contratos simulados, informes y políticas internas sintéticas.

## Demo de escenarios
Presentar casos normales, ambiguos, límite y peligrosos para evaluación futura.

## Demo de crisis
Recorrer crisis sintéticas, línea temporal y decisiones simuladas.

## Demo de revisión humana
Mostrar decisiones de aceptar, corregir, escalar o bloquear en contexto sintético.

## Demo de gemelo digital
Explicar métricas, alertas y consecuencias operativas simuladas.

## Demo de privacidad
Revisar inventario de sensibilidad ficticia, matriz de permisos y riesgos simulados.

## Demo de comparador
Comparar resultados de flujo manual, automatizado clásico y asistido por agente simulado.

## Cierre técnico
Resumen de valor técnico: {resumen['valor_tecnico_del_laboratorio']}

## Límites honestos
- No existe cliente real.
- No se ejecutan agentes reales.
- No existe IA real ni API externa productiva.
- No se emiten recomendaciones empresariales reales.
- No se debe usar como sistema productivo.
"""

