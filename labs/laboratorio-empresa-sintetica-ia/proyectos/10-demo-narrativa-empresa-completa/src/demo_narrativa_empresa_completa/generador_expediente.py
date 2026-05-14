"""Generador de expediente técnico en Markdown para la demo narrativa."""

from __future__ import annotations


def _lista(items: list[str]) -> str:
    if not items:
        return "- Sin elementos asociados en esta ejecución."
    return "\n".join(f"- {x}" for x in items)


def construir_expediente_demo(narrativa: dict) -> str:
    ficha = narrativa["ficha_narrativa_empresa"]
    resumen = narrativa["resumen_ejecutivo_ficticio"]
    hitos = narrativa["linea_tiempo_semanal"]
    episodios = narrativa["episodios_narrativos"]
    evidencias = narrativa["mapa_evidencias"]

    lineas_hitos = "\n".join(
        f"- Día {h['dia']} ({h['fecha_simulada']}): {h['tipo_hito']} | {h['severidad']} | revisión_humana={h['requiere_revision_humana']}"
        for h in hitos
    )
    lineas_episodios = "\n".join(
        f"- {ep['id_episodio']}: {ep['titulo']} | acción={ep['accion_simulada']} | resultado={ep['resultado_simulado']}"
        for ep in episodios
    )
    lineas_evidencias = "\n".join(
        f"- {ev['id_evidencia']} [{ev['proyecto_origen']}] {ev['tipo_evidencia']} -> {ev['ruta_relativa']}"
        for ev in evidencias
    ) or "- No se detectaron evidencias en disco para esta ejecución."

    return f"""# Expediente de Demo Narrativa de Empresa Completa

## Aviso de simulación sintética
Este expediente describe una simulación técnica con datos sintéticos. No representa una operación empresarial real.

## Resumen ejecutivo ficticio
- Empresa simulada: {resumen['empresa_simulada']}
- Semana simulada: {resumen['semana_simulada']}
- Eventos destacados:
{_lista(resumen['eventos_destacados'])}
- Crisis destacadas:
{_lista(resumen['crisis_destacadas'])}
- Alertas principales:
{_lista(resumen['alertas_principales'])}
- Riesgos de privacidad:
{_lista(resumen['riesgos_privacidad'])}
- Revisiones humanas:
{_lista(resumen['revisiones_humanas'])}
- Comparativas relevantes:
{_lista(resumen['comparativas_relevantes'])}

## Descripción de la empresa simulada
- ID demo: {ficha['id_demo']}
- Empresa: {ficha['nombre_empresa']}
- Sector: {ficha['sector']}
- Periodo simulado: {ficha['periodo_simulado']}
- Fecha de generación: {ficha['fecha_generacion']}

## Línea temporal semanal
{lineas_hitos}

## Episodios principales
{lineas_episodios}

## Evidencias generadas por el laboratorio
{lineas_evidencias}

## Lectura técnica del sistema
La integración de proyectos 01 a 10 permite demostrar trazabilidad sintética, correlación entre artefactos y capacidad de construir narrativa evaluable para portfolio técnico.

## Cómo usar esta demo en portfolio
1. Ejecutar todos los proyectos en orden para poblar datos_ejemplo.
2. Ejecutar este proyecto 10 para consolidar narrativa y evidencias.
3. Presentar resultados con el guion de demo y este expediente.

## Límites de uso
- Uso exclusivo para demostración técnica local.
- No aplicar resultados como validación empresarial.
- No inferir decisiones operativas reales a partir de estos datos.

## Nota de alcance real
No existe sistema productivo, no existe cliente real, no existe IA real, no existe API externa, no existe dato real y no existe decisión empresarial real.
"""
