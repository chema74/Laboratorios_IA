import json

from agentes.agente_coordinador import coordinar_tarea
from app.config import RUTA_ESCENARIOS, RUTA_POLITICAS, RUTA_TAREAS
from observabilidad.trazas import Traza

from orquestacion.politicas_accion import cargar_politicas


def _load(path):
    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def ejecutar_escenario(escenario_id: str) -> dict:
    tareas = _load(RUTA_TAREAS)
    escenarios = _load(RUTA_ESCENARIOS)
    politicas = cargar_politicas(_load(RUTA_POLITICAS))

    esc = next((e for e in escenarios if e["id_escenario"] == escenario_id), None)
    if not esc:
        return {"error": f"escenario no encontrado: {escenario_id}"}

    tarea = next((t for t in tareas if t["id_tarea"] == esc["id_tarea"]), None)
    if not tarea:
        return {"error": f"tarea no encontrada: {esc['id_tarea']}"}

    traza = Traza()
    traza.registrar("inicio", {"escenario": escenario_id, "tarea": tarea["id_tarea"]})
    resultado = coordinar_tarea(tarea, politicas, traza)
    traza.registrar("fin", {"estado": resultado.get("estado_final", "desconocido")})
    resultado["trazas"] = traza.eventos
    return resultado
