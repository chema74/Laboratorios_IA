from servicios.modulo_evaluacion_simulado import ejecutar_evaluacion
from servicios.modulo_privacidad_simulado import ejecutar_privacidad
from servicios.modulo_rag_simulado import ejecutar_rag


def enrutar(endpoint: str, payload: dict) -> dict:
    if endpoint == "/rag/consulta":
        return ejecutar_rag(payload)
    if endpoint == "/evaluacion/ejecutar":
        return ejecutar_evaluacion(payload)
    if endpoint == "/privacidad/revisar":
        return ejecutar_privacidad(payload)
    return {"error": "endpoint no soportado"}
