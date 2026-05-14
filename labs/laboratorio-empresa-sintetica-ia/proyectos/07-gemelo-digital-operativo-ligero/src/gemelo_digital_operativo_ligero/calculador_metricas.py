"""Cálculo de métricas operativas sintéticas."""

from __future__ import annotations

from datetime import date


def construir_identidad_empresa(contexto: dict) -> dict:
    empresa = contexto.get("empresa", {}).get("empresa", {})
    return {
        "id_empresa": empresa.get("id_empresa", "EMP-FALLBACK-0001"),
        "nombre": empresa.get("nombre", "Empresa Sintetica Fallback"),
        "sector": empresa.get("sector", "Servicios"),
        "pais": empresa.get("pais", "España"),
        "ciudad": empresa.get("ciudad", "Madrid"),
        "fecha_estado": date.today().isoformat(),
        "origen_simulado": "gemelo_digital_operativo_ligero_v1_local",
    }


def _clamp(valor: float, minimo: float = 0.0, maximo: float = 100.0) -> float:
    return max(minimo, min(maximo, valor))


def calcular_metricas_operativas(contexto: dict) -> dict:
    resumen = contexto.get("empresa", {}).get("resumen_operativo", {})
    eventos = contexto.get("eventos", [])
    crisis = contexto.get("crisis", [])
    revisiones = contexto.get("revisiones", [])
    documentos = contexto.get("documentos", [])
    escenarios = contexto.get("escenarios", [])

    ingresos = float(resumen.get("ingresos_estimados_mensuales", 100000.0))
    tickets_abiertos = int(resumen.get("tickets_abiertos", 0)) + sum(1 for e in eventos if e.get("tipo_evento") == "reclamacion_cliente")
    incidencias_activas = int(resumen.get("incidencias_activas", 0)) + sum(1 for e in eventos if e.get("tipo_evento") in {"retraso_operativo", "alerta_operativa"})
    pagos_pendientes = int(resumen.get("pagos_pendientes", 0)) + sum(1 for e in eventos if e.get("tipo_evento") == "pago_pendiente")
    clientes_en_riesgo = sum(1 for e in eventos if e.get("tipo_evento") in {"cambio_estado_cliente", "reclamacion_cliente"})
    crisis_activas = sum(1 for c in crisis if c.get("estado_crisis") not in {"cerrada_simulada", "contenida"})
    revisiones_pendientes = sum(1 for r in revisiones if r.get("requiere_segunda_revision") or r.get("decision") == "escalar")

    documentos_generados = len(documentos)
    escenarios_disponibles = len(escenarios)

    indice_presion = _clamp((tickets_abiertos * 2.5) + (incidencias_activas * 3.0) + (pagos_pendientes * 1.8) + (crisis_activas * 6.0))
    indice_riesgo = _clamp((clientes_en_riesgo * 3.0) + (crisis_activas * 8.0) + (revisiones_pendientes * 2.0))

    total_trazas = len(eventos) + len(documentos) + len(escenarios) + len(crisis) + len(revisiones)
    trazas_cubiertas = sum(1 for x in crisis if x.get("eventos_relacionados") or x.get("documentos_relacionados")) + len(contexto.get("registro_decisiones", []))
    if total_trazas == 0:
        indice_trazabilidad = 50.0
    else:
        indice_trazabilidad = _clamp((trazas_cubiertas / total_trazas) * 100.0)

    return {
        "ingresos_estimados_mensuales": round(ingresos, 2),
        "tickets_abiertos": tickets_abiertos,
        "incidencias_activas": incidencias_activas,
        "pagos_pendientes": pagos_pendientes,
        "clientes_en_riesgo": clientes_en_riesgo,
        "crisis_activas": crisis_activas,
        "revisiones_pendientes": revisiones_pendientes,
        "documentos_generados": documentos_generados,
        "escenarios_disponibles": escenarios_disponibles,
        "alertas_activas": 0,
        "indice_presion_operativa": round(indice_presion, 2),
        "indice_riesgo_simulado": round(indice_riesgo, 2),
        "indice_trazabilidad": round(indice_trazabilidad, 2),
    }
