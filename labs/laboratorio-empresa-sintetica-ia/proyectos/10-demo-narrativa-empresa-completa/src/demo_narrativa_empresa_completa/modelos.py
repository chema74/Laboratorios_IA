"""Modelos de datos para la demo narrativa de empresa completa."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class FichaNarrativaEmpresa:
    id_demo: str
    nombre_empresa: str
    sector: str
    periodo_simulado: str
    fecha_generacion: str
    origen_simulado: str
    advertencia_sobre_datos_sinteticos: str


@dataclass
class HitoSemanal:
    dia: int
    fecha_simulada: str
    tipo_hito: str
    titulo: str
    descripcion: str
    area_afectada: str
    severidad: str
    artefactos_relacionados: list[str]
    decision_simulada: str
    requiere_revision_humana: bool


@dataclass
class EpisodioNarrativo:
    id_episodio: str
    dia: int
    titulo: str
    contexto: str
    problema_detectado: str
    datos_usados: list[str]
    documentos_relacionados: list[str]
    eventos_relacionados: list[str]
    crisis_relacionadas: list[str]
    revisiones_relacionadas: list[str]
    riesgos_privacidad_relacionados: list[str]
    comparativas_relacionadas: list[str]
    accion_simulada: str
    resultado_simulado: str
    limite_de_uso: str


@dataclass
class EvidenciaMapa:
    id_evidencia: str
    proyecto_origen: str
    tipo_evidencia: str
    ruta_relativa: str
    descripcion: str
    uso_en_demo: str
    es_sintetica: bool


def dataclass_a_dict(objeto: Any) -> dict[str, Any]:
    return asdict(objeto)

