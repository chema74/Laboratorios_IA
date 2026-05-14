"""Modelos de datos para la empresa sintética."""

from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class Empresa:
    id_empresa: str
    nombre: str
    sector: str
    pais: str
    ciudad: str
    moneda: str
    fecha_simulacion: str
    numero_empleados: int
    numero_clientes: int
    numero_productos: int


@dataclass
class Empleado:
    id_empleado: str
    nombre: str
    departamento: str
    rol: str
    nivel_responsabilidad: str
    estado: str


@dataclass
class Cliente:
    id_cliente: str
    nombre: str
    segmento: str
    pais: str
    nivel_riesgo: str
    estado: str


@dataclass
class Producto:
    id_producto: str
    nombre: str
    categoria: str
    precio_base: float
    margen_estimado: float
    estado: str


@dataclass
class ProcesoInterno:
    id_proceso: str
    nombre: str
    area: str
    criticidad: str
    nivel_automatizacion: str
    responsable_ficticio: str


@dataclass
class ResumenOperativo:
    ingresos_estimados_mensuales: float
    tickets_abiertos: int
    incidencias_activas: int
    pagos_pendientes: int
    alertas_operativas: int


def dataclass_a_dict(objeto: Any) -> dict[str, Any]:
    return asdict(objeto)
