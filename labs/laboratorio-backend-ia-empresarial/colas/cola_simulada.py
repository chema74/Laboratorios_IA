class ColaSimulada:
    def __init__(self, tareas=None):
        self._tareas = list(tareas or [])

    def agregar(self, tarea: dict) -> None:
        self._tareas.append({**tarea, "estado": "pendiente"})

    def pendientes(self) -> list[dict]:
        return [t for t in self._tareas if t.get("estado") == "pendiente"]

    def marcar_completada(self, tarea_id: str) -> bool:
        for t in self._tareas:
            if t.get("id") == tarea_id and t.get("estado") == "pendiente":
                t["estado"] = "completada"
                return True
        return False

    def todas(self) -> list[dict]:
        return self._tareas
