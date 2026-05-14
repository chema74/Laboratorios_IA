import re


def _extraer_numeros_y_fechas(texto: str) -> set[str]:
    nums = re.findall(r"\b\d+[\d\./-]*\b", texto)
    return set(nums)


def evaluar_alucinaciones(respuesta_esperada: str, respuesta_candidata: str) -> dict:
    esperada = (respuesta_esperada or "").lower()
    candidata = (respuesta_candidata or "").lower()
    alertas: list[str] = []

    ref_nums = _extraer_numeros_y_fechas(esperada)
    cand_nums = _extraer_numeros_y_fechas(candidata)
    inventados = sorted(cand_nums - ref_nums)
    if inventados:
        alertas.append(f"Cifras/fechas no respaldadas: {inventados}")

    if "política" in candidata and "política" not in esperada:
        alertas.append("Mención a política no presente en la referencia")

    absolutos = ["siempre", "nunca", "garantizado", "todos"]
    if any(a in candidata for a in absolutos):
        alertas.append("Afirmación absoluta potencialmente no respaldada")

    riesgo = min(1.0, 0.25 * len(alertas))
    return {"riesgo": round(riesgo, 4), "alertas": alertas}
