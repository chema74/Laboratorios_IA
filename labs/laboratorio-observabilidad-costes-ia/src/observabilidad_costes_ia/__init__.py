"""Paquete V2.1 de observabilidad y costes de IA."""

from .escenarios import ESCENARIOS_PREDEFINIDOS, obtener_escenario
from .motor import analizar_eventos
from .orquestador import generar_analisis_ejecutivo

__all__ = [
    "analizar_eventos",
    "ESCENARIOS_PREDEFINIDOS",
    "obtener_escenario",
    "generar_analisis_ejecutivo",
]
