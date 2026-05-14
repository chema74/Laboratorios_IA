"""Catálogo controlado de crisis y atributos."""

TIPOS_CRISIS = [
    "caida_ventas",
    "fuga_clientes",
    "retraso_logistico",
    "datos_corruptos",
    "incidente_privacidad",
    "saturacion_operativa",
    "crisis_compuesta",
]

SEVERIDADES = ["baja", "media", "alta", "critica"]
ESTADOS_CRISIS = ["detectada", "en_revision", "contenida", "escalada", "cerrada_simulada"]

DECISIONES_CONTROLADAS = [
    "revisar_datos",
    "escalar_a_humano",
    "bloquear_accion_automatica",
    "generar_informe",
    "priorizar_clientes_en_riesgo",
    "revisar_permisos",
    "auditar_eventos",
    "activar_plan_contingencia_simulado",
]

BASE_CRISIS = {
    "caida_ventas": "Reducción sintética de ingresos y pérdida de pedidos.",
    "fuga_clientes": "Incremento sintético de clientes en riesgo y cancelaciones.",
    "retraso_logistico": "Retrasos sintéticos en entrega, validación y respuesta.",
    "datos_corruptos": "Inconsistencias sintéticas en importes, estados y registros.",
    "incidente_privacidad": "Incidente defensivo sintético por acceso o clasificación incorrecta.",
    "saturacion_operativa": "Acumulación sintética de tickets, alertas y revisiones pendientes.",
    "crisis_compuesta": "Encadenamiento sintético de múltiples crisis en varios días.",
}
