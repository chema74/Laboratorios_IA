"""Paquete de la Fábrica de Documentos Sintéticos."""

from .exportador import exportar_documentos
from .generador import construir_resumen_documentos, generar_documentos_sinteticos

__all__ = [
    "generar_documentos_sinteticos",
    "construir_resumen_documentos",
    "exportar_documentos",
]
