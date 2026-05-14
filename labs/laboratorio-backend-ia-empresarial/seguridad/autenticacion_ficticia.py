def autenticar(usuario: str, token: str, usuarios: list[dict]) -> dict:
    u = next((x for x in usuarios if x["usuario"] == usuario and x["token_ficticio"] == token), None)
    if not u:
        return {"ok": False, "motivo": "credenciales ficticias inválidas"}
    return {"ok": True, "rol": u["rol"]}
