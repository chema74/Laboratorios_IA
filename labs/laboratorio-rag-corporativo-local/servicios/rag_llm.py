from typing import Any

from servicios.pipeline_rag import ejecutar_pipeline


def ejecutar_rag_con_llm(consulta: str) -> dict[str, Any]:
    base = ejecutar_pipeline(consulta)
    fragmentos = []
    for r in base.get("resultados", []):
        f = r.get("fragmento", {})
        fragmentos.append(
            {
                "doc_id": f.get("doc_id"),
                "titulo": f.get("titulo"),
                "contenido": f.get("contenido"),
                "puntuacion": r.get("puntuacion", 0),
            }
        )
    return {"base": base, "fragmentos": fragmentos}
