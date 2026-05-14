def planificar_tarea(tarea: dict) -> dict:
    pasos = [
        {"paso": 1, "accion": "consultar_ticket", "descripcion": "Revisar estado operativo inicial"},
        {"paso": 2, "accion": "consultar_documentacion", "descripcion": "Validar procedimiento interno"},
        {"paso": 3, "accion": "actualizar_crm", "descripcion": "Preparar seguimiento del caso"},
        {"paso": 4, "accion": "coordinar_reunion", "descripcion": "Proponer coordinación interna"},
    ]
    herramientas = ["gestor_tickets_simulado", "base_documental_simulada", "crm_simulado", "calendario_simulado"]
    return {"id_tarea": tarea["id_tarea"], "pasos": pasos, "herramientas": herramientas}
