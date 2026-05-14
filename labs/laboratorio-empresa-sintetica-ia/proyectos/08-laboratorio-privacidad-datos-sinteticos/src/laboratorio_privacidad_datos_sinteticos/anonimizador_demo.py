"""Anonimización determinista de demostración sobre datos sintéticos."""

from __future__ import annotations

import random


def _token_determinista(seed: int, texto: str) -> str:
    azar = random.Random(f"{seed}:{texto}")
    return f"anon_{azar.randrange(10000, 99999)}"


def construir_dataset_anonimizado_demo(dataset_minimizado: dict, seed: int = 42) -> dict:
    """
    Aplica transformación simple demostrativa, no certificada.
    """
    salida: list[dict] = []
    mapa: dict[str, str] = {}

    for fila in dataset_minimizado.get("datos_minimizados", []):
        valor = str(fila["valor_minimizado"])
        campo = fila["campo"].lower()

        if any(x in campo for x in ["id_", "nombre"]):
            if valor not in mapa:
                mapa[valor] = _token_determinista(seed, valor)
            valor_anon = mapa[valor]
            metodo = "tokenizacion_determinista_demo"
        else:
            valor_anon = valor
            metodo = "sin_cambio"

        salida.append(
            {
                "id_dato": fila["id_dato"],
                "campo": fila["campo"],
                "valor_anonimizado": valor_anon,
                "metodo_anonimizacion": metodo,
            }
        )

    return {
        "datos_anonimizados_demo": salida,
        "nota": "Anonimización de demostración sobre datos ya sintéticos. No es anonimización legal real ni certificada.",
    }
