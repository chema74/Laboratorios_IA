import math
import re
from collections import Counter

from app.modelos import ResultadoRecuperacion, Fragmento


def _tokenizar(texto: str) -> list[str]:
    return re.findall(r"[a-zA-ZáéíóúÁÉÍÓÚñÑ0-9]+", texto.lower())


def recuperar_hibrido(consulta: str, fragmentos: list[Fragmento], top_k: int = 5) -> list[ResultadoRecuperacion]:
    tokens_q = _tokenizar(consulta)
    if not tokens_q:
        return []

    docs_tokens = [_tokenizar(f"{f.titulo} {f.contenido} {' '.join(f.etiquetas)}") for f in fragmentos]
    n_docs = max(len(fragmentos), 1)
    avg_len = sum(len(t) for t in docs_tokens) / n_docs

    df = Counter()
    for toks in docs_tokens:
        for t in set(toks):
            df[t] += 1

    resultados: list[ResultadoRecuperacion] = []
    k1, b = 1.2, 0.75
    area_q = set(_tokenizar(consulta))

    for frag, toks in zip(fragmentos, docs_tokens):
        tf = Counter(toks)
        bm25 = 0.0
        for t in tokens_q:
            if t not in tf:
                continue
            idf = math.log(1 + (n_docs - df[t] + 0.5) / (df[t] + 0.5))
            num = tf[t] * (k1 + 1)
            den = tf[t] + k1 * (1 - b + b * (len(toks) / max(avg_len, 1)))
            bm25 += idf * (num / den)

        etiquetas = set(_tokenizar(" ".join(frag.etiquetas)))
        bonus_etiquetas = len(set(tokens_q) & etiquetas) * 0.7
        bonus_area = 0.6 if set(_tokenizar(frag.area)) & area_q else 0.0
        puntuacion = bm25 + bonus_etiquetas + bonus_area

        if puntuacion > 0:
            resultados.append(
                ResultadoRecuperacion(
                    fragmento=frag,
                    puntuacion=round(puntuacion, 4),
                    detalle={"bm25": round(bm25, 4), "bonus_etiquetas": bonus_etiquetas, "bonus_area": bonus_area},
                )
            )

    resultados.sort(key=lambda r: r.puntuacion, reverse=True)
    return resultados[:top_k]
