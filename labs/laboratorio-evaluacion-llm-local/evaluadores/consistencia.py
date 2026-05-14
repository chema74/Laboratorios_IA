import re


def _tokens(texto: str) -> set[str]:
    return set(re.findall(r"[a-zA-ZáéíóúÁÉÍÓÚñÑ0-9]+", (texto or "").lower()))


def evaluar_consistencia(respuesta_esperada: str, respuesta_candidata: str) -> dict:
    esp = _tokens(respuesta_esperada)
    can = _tokens(respuesta_candidata)
    if not esp:
        return {"puntuacion": 0.0, "explicacion": "respuesta esperada vacía"}
    inter = esp & can
    score = len(inter) / len(esp)
    return {
        "puntuacion": round(score, 4),
        "explicacion": f"Coincidencia léxica {len(inter)}/{len(esp)} tokens clave.",
    }
