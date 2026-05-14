from app.modelos import Fragmento


def segmentar_documentos(documentos: list[dict], tamano_fragmento: int = 280) -> list[Fragmento]:
    """Segmenta por longitud fija sin perder trazabilidad documental."""
    fragmentos: list[Fragmento] = []
    for doc in documentos:
        texto = " ".join(str(doc.get("contenido", "")).split())
        if not texto:
            continue
        partes = [texto[i:i + tamano_fragmento] for i in range(0, len(texto), tamano_fragmento)]
        for i, parte in enumerate(partes, start=1):
            fragmentos.append(
                Fragmento(
                    fragmento_id=f"{doc['id']}_f{i}",
                    doc_id=doc["id"],
                    titulo=doc.get("titulo", ""),
                    area=doc.get("area", "general"),
                    etiquetas=doc.get("etiquetas", []),
                    contenido=parte,
                )
            )
    return fragmentos
