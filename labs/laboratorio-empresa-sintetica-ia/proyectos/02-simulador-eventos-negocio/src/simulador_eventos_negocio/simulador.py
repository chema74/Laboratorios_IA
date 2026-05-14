"""Simulador determinista de eventos de negocio ficticios."""

from __future__ import annotations

import random
from collections import Counter
from datetime import date, timedelta

from .modelos import EventoNegocio, ResumenEventos, dataclass_a_dict

TIPOS_EVENTO = [
    "pedido_creado",
    "pago_recibido",
    "pago_pendiente",
    "devolucion_solicitada",
    "reclamacion_cliente",
    "retraso_operativo",
    "cambio_estado_cliente",
    "alerta_operativa",
]


def _seleccionar(azar: random.Random, opciones: list[str]) -> str:
    return opciones[azar.randrange(0, len(opciones))]


def _generar_evento(
    indice: int,
    fecha_evento: date,
    tipo_evento: str,
    azar: random.Random,
    ids_clientes: list[str],
    ids_procesos: list[str],
) -> EventoNegocio:
    severidad = _seleccionar(azar, ["baja", "media", "alta", "critica"])
    estado_evento = _seleccionar(azar, ["abierto", "en_proceso", "resuelto"])

    if tipo_evento in {"pedido_creado", "pago_recibido", "pago_pendiente", "devolucion_solicitada", "reclamacion_cliente", "cambio_estado_cliente"}:
        entidad_afectada = "cliente"
        id_entidad_afectada = _seleccionar(azar, ids_clientes)
    elif tipo_evento == "retraso_operativo":
        entidad_afectada = "proceso"
        id_entidad_afectada = _seleccionar(azar, ids_procesos)
    else:
        entidad_afectada = "operacion"
        id_entidad_afectada = f"OP-{indice:05d}"

    descripcion = f"Evento simulado de tipo {tipo_evento} para entidad {id_entidad_afectada}."
    requiere_revision_humana = severidad in {"alta", "critica"} or tipo_evento in {"reclamacion_cliente", "alerta_operativa"}
    impacto_estimado = round(azar.uniform(50.0, 5000.0), 2)

    return EventoNegocio(
        id_evento=f"EVT-{indice:06d}",
        tipo_evento=tipo_evento,
        fecha_evento=fecha_evento.isoformat(),
        severidad=severidad,
        entidad_afectada=entidad_afectada,
        id_entidad_afectada=id_entidad_afectada,
        descripcion=descripcion,
        estado_evento=estado_evento,
        origen_simulado="simulador_eventos_negocio_v1_local",
        requiere_revision_humana=requiere_revision_humana,
        impacto_estimado=impacto_estimado,
    )


def simular_eventos_negocio(
    empresa: dict,
    seed: int = 42,
    dias: int = 7,
    eventos_por_dia: int = 8,
) -> list[dict]:
    """
    1) Construye contexto mínimo de clientes y procesos.
    2) Genera eventos por día con semilla reproducible.
    3) Devuelve lista serializable de eventos.
    """
    azar = random.Random(seed)

    clientes = empresa.get("clientes", []) or [{"id_cliente": "CLI-0001"}]
    procesos = empresa.get("procesos", []) or [{"id_proceso": "PROC-001"}]
    ids_clientes = [c.get("id_cliente", "CLI-0001") for c in clientes]
    ids_procesos = [p.get("id_proceso", "PROC-001") for p in procesos]

    fecha_inicio = date.today()
    eventos: list[dict] = []
    indice = 1

    for dia in range(dias):
        fecha_actual = fecha_inicio + timedelta(days=dia)
        for _ in range(eventos_por_dia):
            tipo = _seleccionar(azar, TIPOS_EVENTO)
            evento = _generar_evento(indice, fecha_actual, tipo, azar, ids_clientes, ids_procesos)
            eventos.append(dataclass_a_dict(evento))
            indice += 1

    return eventos


def construir_resumen_eventos(eventos: list[dict]) -> dict:
    if not eventos:
        hoy = date.today().isoformat()
        vacio = ResumenEventos(0, {}, {}, 0, 0, hoy, hoy)
        return dataclass_a_dict(vacio)

    tipos = Counter(e["tipo_evento"] for e in eventos)
    severidades = Counter(e["severidad"] for e in eventos)
    revisiones = sum(1 for e in eventos if e.get("requiere_revision_humana"))
    alertas = sum(1 for e in eventos if e.get("tipo_evento") == "alerta_operativa")

    fechas = sorted(e["fecha_evento"] for e in eventos)

    resumen = ResumenEventos(
        total_eventos=len(eventos),
        eventos_por_tipo=dict(tipos),
        eventos_por_severidad=dict(severidades),
        eventos_que_requieren_revision_humana=revisiones,
        alertas_operativas=alertas,
        fecha_inicio_simulacion=fechas[0],
        fecha_fin_simulacion=fechas[-1],
    )
    return dataclass_a_dict(resumen)
