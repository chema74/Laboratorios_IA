PERMISOS = {
    "admin": {"rag", "evaluacion", "privacidad"},
    "tecnico_ia": {"rag", "evaluacion"},
    "auditor": {"evaluacion", "privacidad"},
    "usuario_negocio": {"rag"},
}


def autorizar(rol: str, modulo: str) -> dict:
    ok = modulo in PERMISOS.get(rol, set())
    return {"ok": ok, "motivo": "ok" if ok else "rol sin permiso"}
