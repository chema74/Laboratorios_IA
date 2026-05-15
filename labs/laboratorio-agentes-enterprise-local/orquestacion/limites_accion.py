ACCIONES_BLOQUEADAS = {
    "enviar_correo_real",
    "borrar_datos",
    "modificar_sistema_externo",
    "decision_legal_definitiva",
    "decision_medica_definitiva",
    "decision_financiera_definitiva",
    "ejecutar_compra_real",
}


def validar_accion(accion: str, politicas: dict | None = None) -> tuple[bool, str]:
    if accion in ACCIONES_BLOQUEADAS:
        return False, "accion bloqueada por politica enterprise"
    if politicas is not None:
        if accion not in politicas:
            return False, "accion no declarada en politicas"
        if not bool(politicas[accion]):
            return False, "accion denegada por politicas"
    return True, "ok"
