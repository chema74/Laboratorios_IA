"""Simulador determinista de crisis y línea temporal."""

from __future__ import annotations

import random
from datetime import date, timedelta

from .catalogo_crisis import BASE_CRISIS, DECISIONES_CONTROLADAS, ESTADOS_CRISIS, SEVERIDADES, TIPOS_CRISIS
from .modelos import CrisisSimulada, HitoLineaTiempo, dataclass_a_dict


def _seleccionar(azar: random.Random, opciones: list[str]) -> str:
    return opciones[azar.randrange(0, len(opciones))]


def simular_crisis(contexto: dict, seed: int = 42, numero_crisis: int = 5, dias: int = 10) -> list[dict]:
    """
    1) Selecciona tipos de crisis de catálogo controlado.
    2) Construye crisis con campos obligatorios y valores regulados.
    3) Devuelve lista serializable para exportación.
    """
    azar = random.Random(seed)
    inicio_global = date.today()

    eventos = contexto.get("eventos", []) or [{"id_evento": "EVT-000001"}]
    documentos = contexto.get("documentos", []) or [{"id_documento": "DOC-000001"}]
    escenarios = contexto.get("escenarios", []) or [{"id_escenario": "ESC-000001"}]

    crisis: list[dict] = []

    for i in range(1, numero_crisis + 1):
        tipo = TIPOS_CRISIS[(i - 1) % len(TIPOS_CRISIS)]
        fecha_inicio = inicio_global + timedelta(days=azar.randrange(0, max(dias, 1)))
        duracion = azar.randrange(2, min(max(dias, 3), 12))
        fecha_fin = fecha_inicio + timedelta(days=duracion)

        evento = eventos[(i - 1) % len(eventos)]
        doc = documentos[(i - 1) % len(documentos)]
        esc = escenarios[(i - 1) % len(escenarios)]

        severidad = _seleccionar(azar, SEVERIDADES)
        estado = _seleccionar(azar, ESTADOS_CRISIS)
        decisiones = azar.sample(DECISIONES_CONTROLADAS, k=3)
        riesgos = ["efecto_reputacional", "acumulacion_backlog", "errores_decision"]

        item = CrisisSimulada(
            id_crisis=f"CRS-{i:05d}",
            tipo_crisis=tipo,
            titulo=f"Crisis simulada {tipo.replace('_', ' ')} {i}",
            descripcion=BASE_CRISIS[tipo],
            fecha_inicio=fecha_inicio.isoformat(),
            fecha_fin_estimada=fecha_fin.isoformat(),
            severidad=severidad,
            areas_afectadas=",".join(sorted(set(["operaciones", "finanzas", "atencion_cliente"]))),
            entidades_afectadas=",".join(["clientes", "procesos"]),
            eventos_relacionados=evento.get("id_evento", "EVT-000001"),
            documentos_relacionados=doc.get("id_documento", "DOC-000001"),
            escenarios_relacionados=esc.get("id_escenario", "ESC-000001"),
            indicadores_impacto="ingresos,pagos_pendientes,tickets_abiertos,alertas",
            senales_tempranas="variacion_negativa,incremento_retrasos,incremento_reclamaciones",
            decisiones_recomendadas=",".join(decisiones),
            riesgos_secundarios=",".join(riesgos),
            requiere_revision_humana=(severidad in {"alta", "critica"} or tipo in {"incidente_privacidad", "datos_corruptos", "crisis_compuesta"}),
            estado_crisis=estado,
            origen_simulado="motor_simulacion_crisis_v1_local",
        )
        crisis.append(dataclass_a_dict(item))

    return crisis


def generar_linea_tiempo(crisis: list[dict], seed: int = 42) -> list[dict]:
    """
    1) Recorre cada crisis y crea hitos diarios simulados.
    2) Mantiene decisiones pendientes dentro del catálogo controlado.
    """
    azar = random.Random(seed + 1000)
    linea: list[dict] = []

    for item in crisis:
        inicio = date.fromisoformat(item["fecha_inicio"])
        fin = date.fromisoformat(item["fecha_fin_estimada"])
        total_dias = max(1, (fin - inicio).days)

        for d in range(total_dias + 1):
            fecha = inicio + timedelta(days=d)
            decision = _seleccionar(azar, DECISIONES_CONTROLADAS)
            hito = HitoLineaTiempo(
                fecha=fecha.isoformat(),
                id_crisis=item["id_crisis"],
                tipo_hito=_seleccionar(azar, ["deteccion", "contencion", "revision", "seguimiento"]),
                descripcion=f"Hito simulado {d + 1} de la crisis {item['id_crisis']}.",
                impacto_estimado=round(azar.uniform(100.0, 9000.0), 2),
                decision_pendiente=decision,
                requiere_revision_humana=bool(item["requiere_revision_humana"]),
            )
            linea.append(dataclass_a_dict(hito))

    return linea
