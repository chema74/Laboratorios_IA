"""Generador determinista de empresa sintética."""

from __future__ import annotations

import random
from datetime import date

from .modelos import (
    Cliente,
    Empleado,
    Empresa,
    ProcesoInterno,
    Producto,
    ResumenOperativo,
    dataclass_a_dict,
)


def _seleccionar(azar: random.Random, opciones: list[str]) -> str:
    return opciones[azar.randrange(0, len(opciones))]


def generar_empresa_sintetica(
    seed: int = 42,
    numero_empleados: int = 10,
    numero_clientes: int = 20,
    numero_productos: int = 8,
) -> dict:
    """
    1) Inicializa random local con semilla para reproducibilidad.
    2) Genera entidades ficticias coherentes.
    3) Calcula un resumen operativo básico.
    """
    azar = random.Random(seed)

    sectores = ["Logistica", "Retail", "Salud", "Educacion", "Manufactura"]
    paises = ["España", "México", "Colombia", "Chile", "Perú"]
    ciudades = ["Madrid", "Barcelona", "Valencia", "Sevilla", "Bilbao"]
    monedas = ["EUR", "USD", "MXN", "COP"]

    departamentos = ["Operaciones", "Ventas", "Finanzas", "Atencion Cliente", "TI"]
    roles = ["Analista", "Coordinador", "Especialista", "Responsable", "Tecnico"]
    niveles_responsabilidad = ["Bajo", "Medio", "Alto"]

    segmentos_cliente = ["PYME", "Corporativo", "Startup", "Publico"]
    niveles_riesgo = ["Bajo", "Medio", "Alto"]

    categorias_producto = ["Servicio", "Software", "Soporte", "Consultoria"]
    estados = ["activo", "inactivo", "en_revision"]
    estados_cliente = ["activo", "en_revision", "bloqueado"]

    procesos_base = [
        ("Gestion de pedidos", "Operaciones"),
        ("Facturacion", "Finanzas"),
        ("Soporte al cliente", "Atencion Cliente"),
        ("Control de inventario", "Operaciones"),
        ("Onboarding de clientes", "Ventas"),
    ]

    empresa = Empresa(
        id_empresa=f"EMP-{seed:04d}",
        nombre=f"Empresa Sintetica {seed}",
        sector=_seleccionar(azar, sectores),
        pais=_seleccionar(azar, paises),
        ciudad=_seleccionar(azar, ciudades),
        moneda=_seleccionar(azar, monedas),
        fecha_simulacion=date.today().isoformat(),
        numero_empleados=numero_empleados,
        numero_clientes=numero_clientes,
        numero_productos=numero_productos,
    )

    empleados: list[Empleado] = []
    for i in range(1, numero_empleados + 1):
        empleados.append(
            Empleado(
                id_empleado=f"EMPLO-{i:04d}",
                nombre=f"Empleado Ficticio {i}",
                departamento=_seleccionar(azar, departamentos),
                rol=_seleccionar(azar, roles),
                nivel_responsabilidad=_seleccionar(azar, niveles_responsabilidad),
                estado=_seleccionar(azar, estados),
            )
        )

    clientes: list[Cliente] = []
    for i in range(1, numero_clientes + 1):
        clientes.append(
            Cliente(
                id_cliente=f"CLI-{i:04d}",
                nombre=f"Cliente Ficticio {i}",
                segmento=_seleccionar(azar, segmentos_cliente),
                pais=_seleccionar(azar, paises),
                nivel_riesgo=_seleccionar(azar, niveles_riesgo),
                estado=_seleccionar(azar, estados_cliente),
            )
        )

    productos: list[Producto] = []
    for i in range(1, numero_productos + 1):
        precio = round(azar.uniform(100.0, 5000.0), 2)
        margen = round(azar.uniform(0.1, 0.6), 2)
        productos.append(
            Producto(
                id_producto=f"PROD-{i:04d}",
                nombre=f"Producto Sintetico {i}",
                categoria=_seleccionar(azar, categorias_producto),
                precio_base=precio,
                margen_estimado=margen,
                estado=_seleccionar(azar, estados),
            )
        )

    procesos: list[ProcesoInterno] = []
    for i, (nombre_proceso, area) in enumerate(procesos_base, start=1):
        responsable = _seleccionar(azar, [e.nombre for e in empleados]) if empleados else "No asignado"
        procesos.append(
            ProcesoInterno(
                id_proceso=f"PROC-{i:03d}",
                nombre=nombre_proceso,
                area=area,
                criticidad=_seleccionar(azar, ["Baja", "Media", "Alta"]),
                nivel_automatizacion=_seleccionar(azar, ["Manual", "Semiautomatizado", "Automatizado"]),
                responsable_ficticio=responsable,
            )
        )

    ingresos_estimados = round(sum(p.precio_base for p in productos) * azar.uniform(1.5, 4.5), 2)
    resumen = ResumenOperativo(
        ingresos_estimados_mensuales=ingresos_estimados,
        tickets_abiertos=max(1, numero_clientes // 4),
        incidencias_activas=max(1, numero_empleados // 6),
        pagos_pendientes=max(1, numero_clientes // 5),
        alertas_operativas=max(1, len(procesos) // 2),
    )

    return {
        "empresa": dataclass_a_dict(empresa),
        "empleados": [dataclass_a_dict(x) for x in empleados],
        "clientes": [dataclass_a_dict(x) for x in clientes],
        "productos": [dataclass_a_dict(x) for x in productos],
        "procesos": [dataclass_a_dict(x) for x in procesos],
        "resumen_operativo": dataclass_a_dict(resumen),
    }
