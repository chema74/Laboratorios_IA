"""Paquete del Comparador entre Agente y Proceso."""

from .catalogo_procesos import construir_procesos_comparados
from .simulador_flujos import simular_resultados_flujos
from .comparador import construir_comparaciones

__all__ = [
    "construir_procesos_comparados",
    "simular_resultados_flujos",
    "construir_comparaciones",
]
