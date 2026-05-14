def modulo_por_endpoint(endpoint: str) -> str:
    if endpoint.startswith("/rag"):
        return "rag"
    if endpoint.startswith("/evaluacion"):
        return "evaluacion"
    if endpoint.startswith("/privacidad"):
        return "privacidad"
    return "desconocido"
