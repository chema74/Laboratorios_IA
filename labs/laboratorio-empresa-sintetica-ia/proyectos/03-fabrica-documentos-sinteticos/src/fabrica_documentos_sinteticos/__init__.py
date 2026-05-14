"""Paquete de la Fábrica de Documentos Sintéticos."""

from .generador import generar_documentos_sinteticos, construir_resumen_documentos
from .exportador import exportar_documentos

__all__ = [
    "generar_documentos_sinteticos",
    "construir_resumen_documentos",
    "exportar_documentos",
]
