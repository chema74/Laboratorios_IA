from herramientas.base_documental_simulada import buscar_documento
from herramientas.calendario_simulado import proponer_reunion
from herramientas.crm_simulado import consultar_cliente
from herramientas.gestor_tickets_simulado import buscar_tickets
from orquestacion.limites_accion import validar_accion


def ejecutar_plan(plan: dict, politicas: dict | None = None) -> dict:
    resultados = []
    bloqueos = []
    for p in plan["pasos"]:
        accion = p["accion"]
        ok, motivo = validar_accion(accion, politicas)
        if not ok:
            bloqueos.append({"paso": p["paso"], "accion": accion, "motivo": motivo})
            continue

        if accion == "consultar_ticket":
            salida = buscar_tickets("soporte_tic")
        elif accion == "consultar_documentacion":
            salida = buscar_documento("soporte_tic")
        elif accion == "actualizar_crm":
            salida = consultar_cliente("CLI-001")
        elif accion == "coordinar_reunion":
            salida = proponer_reunion("equipo_tic")
        else:
            salida = {"info": "acción no implementada en V1"}

        resultados.append({"paso": p["paso"], "accion": accion, "salida": salida})
    return {"resultados": resultados, "bloqueos": bloqueos}
