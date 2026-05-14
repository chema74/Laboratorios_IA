"""Evaluación de consecuencias y resumen del gemelo digital."""

from __future__ import annotations

from collections import Counter
from datetime import date

from .modelos import ConsecuenciaOperativa, dataclass_a_dict


def generar_consecuencias_operativas(alertas: list[dict], decisiones: list[dict]) -> list[dict]:
    consecuencias: list[dict] = []

    for i, dec in enumerate(decisiones, start=1):
        if dec["estado_decision"] == "aceptada_simulada":
            impacto = "mejora_parcial"
            riesgo_residual = "medio"
        elif dec["estado_decision"] == "escalada":
            impacto = "contencion_en_revision"
            riesgo_residual = "alto"
        else:
            impacto = "impacto_indeterminado"
            riesgo_residual = "medio"

        cons = ConsecuenciaOperativa(
            id_consecuencia=f"CON-{i:05d}",
            origen=dec["id_decision"],
            descripcion=f"Consecuencia simulada derivada de la decisión {dec['id_decision']}.",
            area_afectada=dec["area_responsable"],
            impacto_estimado=impacto,
            horizonte_temporal="corto_plazo_simulado",
            riesgo_residual=riesgo_residual,
            accion_de_seguimiento="revisar_estado_en_proxima_iteracion",
        )
        consecuencias.append(dataclass_a_dict(cons))

    if not consecuencias and alertas:
        cons = ConsecuenciaOperativa(
            id_consecuencia="CON-00001",
            origen=alertas[0]["id_alerta"],
            descripcion="Consecuencia sintética por alerta sin decisión asociada.",
            area_afectada=alertas[0]["area_afectada"],
            impacto_estimado="impacto_bajo",
            horizonte_temporal="corto_plazo_simulado",
            riesgo_residual="bajo",
            accion_de_seguimiento="mantener_observacion",
        )
        consecuencias.append(dataclass_a_dict(cons))

    return consecuencias


def construir_resumen_gemelo(estado: dict, consecuencias: list[dict], entradas_utilizadas: dict[str, str]) -> dict:
    alertas = estado["alertas_operativas"]
    decisiones = estado["decisiones_simuladas"]
    areas = estado["estado_por_areas"]
    metricas = estado["metricas_operativas"]

    severidad = Counter(a["severidad"] for a in alertas)
    estados_decision = Counter(d["estado_decision"] for d in decisiones)

    areas_presion = sorted(areas.items(), key=lambda x: x[1]["nivel_presion"], reverse=True)
    areas_top = [a[0] for a in areas_presion[:3]]

    return {
        "fecha_generacion": date.today().isoformat(),
        "empresa": estado["identidad_empresa"],
        "total_alertas": len(alertas),
        "alertas_por_severidad": dict(severidad),
        "total_decisiones_simuladas": len(decisiones),
        "decisiones_por_estado": dict(estados_decision),
        "total_consecuencias": len(consecuencias),
        "areas_con_mayor_presion": areas_top,
        "indice_presion_operativa": metricas["indice_presion_operativa"],
        "indice_riesgo_simulado": metricas["indice_riesgo_simulado"],
        "indice_trazabilidad": metricas["indice_trazabilidad"],
        "entradas_utilizadas": entradas_utilizadas,
        "advertencia_sobre_datos_sinteticos": "Gemelo digital sintético para pruebas internas. No representa operación real.",
        "advertencia_sobre_no_monitorizacion_real": "No existe monitorización real ni toma de decisión empresarial real.",
    }


def construir_expediente_estado_operativo(estado: dict, consecuencias: list[dict], resumen: dict) -> str:
    metricas = estado["metricas_operativas"]
    areas = estado["estado_por_areas"]
    alertas = estado["alertas_operativas"]
    decisiones = estado["decisiones_simuladas"]
    linea = estado["linea_tiempo_operativa"]

    lista_areas = "\n".join([f"- {k}: estado={v['estado_area']} | presion={v['nivel_presion']}" for k, v in areas.items()])
    lista_alertas = "\n".join([f"- {a['id_alerta']} | {a['tipo_alerta']} | {a['severidad']} | {a['estado_alerta']}" for a in alertas])
    lista_decisiones = "\n".join([f"- {d['id_decision']} | {d['estado_decision']} | {d['area_responsable']}" for d in decisiones])
    lista_consecuencias = "\n".join([f"- {c['id_consecuencia']} | {c['area_afectada']} | {c['impacto_estimado']}" for c in consecuencias])
    lista_hitos = "\n".join([f"- {h['fecha']} | {h['tipo_hito']} | {h['area_afectada']} | {h['severidad']}" for h in linea[:12]])

    return (
        "# Expediente de Estado Operativo Simulado\n\n"
        "**Aviso:** Simulación sintética para portfolio técnico. No es monitorización real.\n\n"
        "## Resumen ejecutivo ficticio\n"
        f"Estado consolidado para {resumen['empresa']['nombre']} con {resumen['total_alertas']} alertas y {resumen['total_decisiones_simuladas']} decisiones simuladas.\n\n"
        "## Métricas principales\n"
        f"- indice_presion_operativa: {metricas['indice_presion_operativa']}\n"
        f"- indice_riesgo_simulado: {metricas['indice_riesgo_simulado']}\n"
        f"- indice_trazabilidad: {metricas['indice_trazabilidad']}\n\n"
        "## Estado por áreas\n"
        f"{lista_areas}\n\n"
        "## Alertas activas\n"
        f"{lista_alertas}\n\n"
        "## Decisiones simuladas\n"
        f"{lista_decisiones}\n\n"
        "## Consecuencias operativas simuladas\n"
        f"{lista_consecuencias}\n\n"
        "## Línea temporal resumida\n"
        f"{lista_hitos}\n\n"
        "## Límites de uso\n"
        "- No usar para operación real.\n"
        "- No usar para monitorización real.\n"
        "- No usar para decisiones empresariales reales.\n\n"
        "## Nota final\n"
        "No existe monitorización real ni decisión empresarial real en este gemelo digital.\n"
    )
