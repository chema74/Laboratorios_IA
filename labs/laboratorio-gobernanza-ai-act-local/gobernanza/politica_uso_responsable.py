def generar_politica() -> dict:
    return {
        "usos_permitidos": ["asistencia documental interna", "resumen operativo", "soporte a decisiones no definitivas"],
        "usos_prohibidos": ["decisiones legales definitivas", "decisiones médicas definitivas", "decisiones financieras definitivas"],
        "tratamiento_datos": "Minimización de datos y revisión humana obligatoria en casos críticos.",
        "supervision_humana": "Requerida en clasificación de riesgo alto orientativo y revisión obligatoria.",
        "escalado_riesgos": "Escalar al responsable de gobernanza y cumplimiento interno.",
    }
