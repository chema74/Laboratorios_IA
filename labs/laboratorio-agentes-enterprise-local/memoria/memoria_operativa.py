class MemoriaOperativa:
    def __init__(self) -> None:
        self._eventos: list[dict] = []

    def registrar(self, evento: dict) -> None:
        self._eventos.append(evento)

    def consultar(self) -> list[dict]:
        return list(self._eventos)
