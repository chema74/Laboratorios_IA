ACCIONES_BLOQUEADAS = {
    "enviar_correo_real",
    "borrar_datos",
    "modificar_sistema_externo",
    "decision_legal_definitiva",
    "decision_medica_definitiva",
    "decision_financiera_definitiva",
    "ejecutar_compra_real",
}


def validar_accion(accion: str) -> tuple[bool, str]:
    if accion in ACCIONES_BLOQUEADAS:
        return False, "acción bloqueada por política enterprise"
    return True, "ok"
