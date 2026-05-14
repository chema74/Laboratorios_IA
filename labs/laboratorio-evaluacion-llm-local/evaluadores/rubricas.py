def normalizar(valor: float) -> float:
    return max(0.0, min(1.0, round(valor, 4)))


def puntuar_rubricas(consistencia: float, cobertura: float, claridad: float, trazabilidad: float, ausencia_invencion: float, precision: float) -> dict:
    return {
        "consistencia": normalizar(consistencia),
        "cobertura": normalizar(cobertura),
        "claridad": normalizar(claridad),
        "trazabilidad": normalizar(trazabilidad),
        "ausencia_invencion": normalizar(ausencia_invencion),
        "precision": normalizar(precision),
    }
