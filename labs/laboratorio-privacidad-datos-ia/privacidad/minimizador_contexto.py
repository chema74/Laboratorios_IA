import json


def minimizar_contexto(payload: dict, campos_permitidos: list[str] | None = None) -> dict:
    permitidos = campos_permitidos or ["caso_uso", "objetivo", "texto"]
    reducido = {k: v for k, v in payload.items() if k in permitidos}
    eliminados = [k for k in payload.keys() if k not in permitidos]
    texto = json.dumps(reducido, ensure_ascii=False)
    return {"contexto_minimizado": reducido, "texto_minimizado": texto, "explicacion": f"Campos eliminados: {eliminados}"}
