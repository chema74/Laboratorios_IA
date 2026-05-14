from app.config import MAX_CARACTERES_CONSULTA

TERMINOS_FUERA_DOMINIO = {"horoscopo", "futbol", "criptomonedas", "receta", "videojuego"}


def validar_consulta(consulta: str) -> tuple[bool, str]:
    q = (consulta or "").strip()
    if not q:
        return False, "consulta vacía"
    if len(q) > MAX_CARACTERES_CONSULTA:
        return False, "consulta demasiado larga"
    q_low = q.lower()
    if any(t in q_low for t in TERMINOS_FUERA_DOMINIO):
        return False, "consulta fuera de dominio corporativo"
    return True, "ok"
