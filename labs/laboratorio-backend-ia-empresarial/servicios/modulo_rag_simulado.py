def ejecutar_rag(payload: dict) -> dict:
    q = payload.get("consulta", "")
    return {"modulo": "rag", "respuesta": f"Resultado RAG simulado para: {q}", "confianza": 0.82}
