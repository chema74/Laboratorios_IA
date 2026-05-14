"""Construcción de dataset minimizado para pruebas sintéticas."""

from __future__ import annotations


def construir_dataset_minimizado(inventario: list[dict]) -> dict:
    """
    1) Filtra campos críticos o no necesarios.
    2) Conserva trazabilidad de exclusión o resumen.
    """
    datos_minimizados: list[dict] = []
    trazabilidad: list[dict] = []

    for d in inventario:
        if d["nivel_sensibilidad_ficticia"] == "critica":
            trazabilidad.append(
                {
                    "id_dato": d["id_dato"],
                    "campo": d["campo"],
                    "accion": "eliminado",
                    "motivo": "nivel_critico",
                }
            )
            continue

        valor = d["valor_simulado_resumido"]
        accion = "conservado"
        if d["requiere_minimizacion"]:
            valor = f"resumen::{valor[:15]}"
            accion = "resumido"

        datos_minimizados.append(
            {
                "id_dato": d["id_dato"],
                "origen": d["origen"],
                "tipo_entidad": d["tipo_entidad"],
                "campo": d["campo"],
                "valor_minimizado": valor,
                "nivel_sensibilidad_ficticia": d["nivel_sensibilidad_ficticia"],
            }
        )
        trazabilidad.append(
            {
                "id_dato": d["id_dato"],
                "campo": d["campo"],
                "accion": accion,
                "motivo": "regla_minimizacion",
            }
        )

    return {
        "datos_minimizados": datos_minimizados,
        "trazabilidad_minimizacion": trazabilidad,
    }
