def registrar_contexto(memoria, tipo: str, contenido: dict) -> None:
    memoria.registrar({"tipo": tipo, "contenido": contenido})
