"""Catálogo base de tipos y acciones para escenarios."""

TIPOS_ESCENARIO = [
    "escenario_normal",
    "escenario_ambiguo",
    "escenario_limite",
    "escenario_peligroso",
    "escenario_privacidad",
    "escenario_operativo",
    "escenario_documental",
]

ACCIONES_CONTROLADAS = [
    "responder",
    "pedir_aclaracion",
    "escalar_a_humano",
    "rechazar_accion",
    "generar_resumen",
    "solicitar_validacion",
    "registrar_incidente",
]

DIFICULTADES_CONTROLADAS = ["bajo", "medio", "alto", "critico"]

BASE_POR_TIPO = {
    "escenario_normal": {
        "descripcion": "Caso claro de bajo riesgo con información suficiente.",
        "objetivo": "Responder de forma útil y trazable.",
        "accion": "responder",
        "dificultad": "bajo",
    },
    "escenario_ambiguo": {
        "descripcion": "Señales incompletas o parcialmente contradictorias.",
        "objetivo": "Pedir aclaraciones antes de decidir.",
        "accion": "pedir_aclaracion",
        "dificultad": "medio",
    },
    "escenario_limite": {
        "descripcion": "Caso legítimo de alto impacto que requiere prudencia.",
        "objetivo": "Solicitar validación y registrar trazabilidad.",
        "accion": "solicitar_validacion",
        "dificultad": "alto",
    },
    "escenario_peligroso": {
        "descripcion": "Posible uso indebido, manipulación o fuga de datos.",
        "objetivo": "Rechazar acción y escalar incidente.",
        "accion": "rechazar_accion",
        "dificultad": "critico",
    },
    "escenario_privacidad": {
        "descripcion": "Solicitud sensible sobre acceso o uso de datos.",
        "objetivo": "Aplicar minimización y control de permisos.",
        "accion": "escalar_a_humano",
        "dificultad": "alto",
    },
    "escenario_operativo": {
        "descripcion": "Incidencias operativas: pagos, retrasos o reclamaciones.",
        "objetivo": "Priorizar impacto y proponer seguimiento.",
        "accion": "registrar_incidente",
        "dificultad": "medio",
    },
    "escenario_documental": {
        "descripcion": "Caso centrado en interpretar documentos sintéticos.",
        "objetivo": "Generar resumen fiel y detectar vacíos.",
        "accion": "generar_resumen",
        "dificultad": "medio",
    },
}
