import re

from app.modelos import ResultadoRecuperacion


def _tok(texto: str) -> set[str]:
    return set(re.findall(r"[a-zA-ZáéíóúÁÉÍÓÚñÑ0-9]+", texto.lower()))


def reordenar_resultados(consulta: str, resultados: list[ResultadoRecuperacion]) -> list[ResultadoRecuperacion]:
    consulta_t = _tok(consulta)

    def clave(res: ResultadoRecuperacion) -> tuple[float, int, int]:
        area_match = 1 if _tok(res.fragmento.area) & consulta_t else 0
        term_match = len(_tok(res.fragmento.contenido) & consulta_t)
        return (res.puntuacion, area_match, term_match)

    return sorted(resultados, key=clave, reverse=True)
