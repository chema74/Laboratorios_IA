"""Paquete del Motor de Simulación de Crisis."""

from .simulador import simular_crisis, generar_linea_tiempo
from .evaluador_impacto import construir_resumen_crisis
from .exportador import exportar_resultados_crisis

__all__ = [
    "simular_crisis",
    "generar_linea_tiempo",
    "construir_resumen_crisis",
    "exportar_resultados_crisis",
]
