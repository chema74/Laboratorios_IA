"""Catálogos controlados para decisiones de revisión humana simulada."""

TIPOS_ELEMENTO = [
    "evento_negocio",
    "documento_sintetico",
    "escenario_prueba_agente",
    "crisis_simulada",
]

DECISIONES_CONTROLADAS = [
    "aceptar",
    "rechazar",
    "corregir",
    "escalar",
    "solicitar_mas_informacion",
    "registrar_incidente",
    "bloquear_accion",
]

ACCIONES_POSTERIORES_CONTROLADAS = [
    "cerrar_revision",
    "enviar_a_revision_senior",
    "devolver_para_correccion",
    "generar_informe",
    "bloquear_automatizacion",
    "abrir_incidencia",
    "mantener_observacion",
]

NIVELES_CONFIANZA = ["baja", "media", "alta"]

ROLES_REVISORES = [
    "responsable_operaciones",
    "responsable_comercial",
    "responsable_datos",
    "responsable_privacidad",
    "responsable_tecnico",
    "direccion",
]

ESTADOS_REGISTRO = ["registrado", "pendiente", "escalado", "cerrado_simulado"]

CRITERIOS_BASE = [
    "consistencia_datos",
    "trazabilidad",
    "riesgo_operativo",
    "sensibilidad_ficticia",
    "claridad_documental",
    "cumplimiento_politica_interna",
]

MAPEO_ACCION_POR_DECISION = {
    "aceptar": "cerrar_revision",
    "rechazar": "abrir_incidencia",
    "corregir": "devolver_para_correccion",
    "escalar": "enviar_a_revision_senior",
    "solicitar_mas_informacion": "mantener_observacion",
    "registrar_incidente": "generar_informe",
    "bloquear_accion": "bloquear_automatizacion",
}
