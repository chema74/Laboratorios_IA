from agentes.agente_ejecutor import ejecutar_plan
from agentes.agente_planificador import planificar_tarea
from agentes.agente_revisor import revisar_resultados
from memoria.memoria_operativa import MemoriaOperativa
from memoria.registro_contexto import registrar_contexto


def coordinar_tarea(tarea: dict, politicas: dict, traza) -> dict:
    memoria = MemoriaOperativa()
    plan = planificar_tarea(tarea)
    traza.registrar("planificacion", {"pasos": len(plan["pasos"])})
    registrar_contexto(memoria, "plan", plan)

    ejecucion = ejecutar_plan(plan)
    traza.registrar("ejecucion", {"resultados": len(ejecucion["resultados"]), "bloqueos": len(ejecucion["bloqueos"])})
    registrar_contexto(memoria, "ejecucion", ejecucion)

    revision = revisar_resultados(ejecucion)
    traza.registrar("revision", revision)
    registrar_contexto(memoria, "revision", revision)

    return {
        "id_tarea": tarea["id_tarea"],
        "plan": plan,
        "ejecucion": ejecucion,
        "revision": revision,
        "estado_final": revision["estado"],
        "politicas_cargadas": len(politicas),
        "memoria": memoria.consultar(),
    }
