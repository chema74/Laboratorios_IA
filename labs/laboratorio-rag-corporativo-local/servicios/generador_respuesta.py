from app.modelos import ResultadoRecuperacion


def generar_respuesta_extractiva(consulta: str, resultados: list[ResultadoRecuperacion]) -> dict:
    if not resultados:
        return {
            "respuesta": "No encontré evidencia suficiente en el corpus local para responder con confianza.",
            "citas": [],
        }

    top = resultados[:2]
    frases = []
    citas = []
    for r in top:
        extracto = r.fragmento.contenido[:180].strip()
        frases.append(f"{r.fragmento.titulo}: {extracto}...")
        citas.append(f"{r.fragmento.doc_id}#{r.fragmento.fragmento_id}")

    respuesta = f"Consulta: '{consulta}'. Evidencia encontrada: " + " | ".join(frases)
    return {"respuesta": respuesta, "citas": citas}
