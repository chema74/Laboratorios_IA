"""Carga de empresa sintética desde JSON con fallback interno."""

from __future__ import annotations

import json
from pathlib import Path


def _empresa_fallback() -> dict:
    """Define datos mínimos internos para no depender de una demo previa."""
    return {
        "empresa": {
            "id_empresa": "EMP-FALLBACK-0001",
            "nombre": "Empresa Sintetica Fallback",
            "sector": "Servicios",
            "pais": "España",
            "ciudad": "Madrid",
            "moneda": "EUR",
            "fecha_simulacion": "2026-01-01",
            "numero_empleados": 5,
            "numero_clientes": 6,
            "numero_productos": 4,
        },
        "empleados": [
            {"id_empleado": "EMPLO-0001", "nombre": "Empleado Ficticio 1"},
            {"id_empleado": "EMPLO-0002", "nombre": "Empleado Ficticio 2"},
        ],
        "clientes": [
            {"id_cliente": "CLI-0001", "nombre": "Cliente Ficticio 1", "estado": "activo"},
            {"id_cliente": "CLI-0002", "nombre": "Cliente Ficticio 2", "estado": "en_revision"},
            {"id_cliente": "CLI-0003", "nombre": "Cliente Ficticio 3", "estado": "activo"},
        ],
        "productos": [
            {"id_producto": "PROD-0001", "nombre": "Producto Sintetico 1", "precio_base": 1000.0},
            {"id_producto": "PROD-0002", "nombre": "Producto Sintetico 2", "precio_base": 650.0},
        ],
        "procesos": [
            {"id_proceso": "PROC-001", "nombre": "Gestion de pedidos", "criticidad": "Alta"},
            {"id_proceso": "PROC-002", "nombre": "Facturacion", "criticidad": "Media"},
        ],
    }


def cargar_empresa_sintetica(ruta_entrada: str | Path) -> dict:
    """
    1) Intenta cargar JSON de empresa existente.
    2) Si no existe o falla el parseo, utiliza fallback interno.
    """
    ruta = Path(ruta_entrada)
    if ruta.exists() and ruta.is_file():
        try:
            with ruta.open("r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
            if isinstance(datos, dict) and "empresa" in datos:
                return datos
        except (json.JSONDecodeError, OSError):
            pass

    return _empresa_fallback()
