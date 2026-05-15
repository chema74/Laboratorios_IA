"""Paquete del Comparador entre Agente y Proceso."""

from .catalogo_procesos import construir_procesos_comparados
from .comparador import construir_comparaciones
from .simulador_flujos import simular_resultados_flujos

__all__ = [
    "construir_procesos_comparados",
    "simular_resultados_flujos",
    "construir_comparaciones",
]
