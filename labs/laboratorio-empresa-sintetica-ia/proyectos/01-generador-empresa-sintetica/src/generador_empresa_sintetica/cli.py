"""Interfaz CLI para generar y exportar una empresa sintética."""

from __future__ import annotations

import argparse
from pathlib import Path

from .exportador import exportar_empresa_json, exportar_tablas_csv
from .generador import generar_empresa_sintetica


def crear_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generador local de empresa sintética")
    parser.add_argument("--seed", type=int, default=42, help="Semilla para generación reproducible")
    parser.add_argument("--empleados", type=int, default=10, help="Número de empleados ficticios")
    parser.add_argument("--clientes", type=int, default=20, help="Número de clientes ficticios")
    parser.add_argument("--productos", type=int, default=8, help="Número de productos ficticios")
    parser.add_argument("--salida", type=str, default="datos_ejemplo/empresa_sintetica_demo", help="Carpeta de salida")
    return parser


def ejecutar_desde_argumentos(args: argparse.Namespace) -> dict:
    """
    1) Generar datos sintéticos con parámetros de entrada.
    2) Exportar JSON completo.
    3) Exportar tablas CSV de entidades principales.
    """
    resultado = generar_empresa_sintetica(
        seed=args.seed,
        numero_empleados=args.empleados,
        numero_clientes=args.clientes,
        numero_productos=args.productos,
    )

    ruta_salida = Path(args.salida)
    json_ruta = exportar_empresa_json(resultado, ruta_salida)
    csv_rutas = exportar_tablas_csv(resultado, ruta_salida)

    print("Generación completada correctamente.")
    print(f"Archivo JSON: {json_ruta}")
    print("Archivos CSV:")
    for ruta in csv_rutas:
        print(f"- {ruta}")

    return resultado


def main() -> None:
    parser = crear_parser()
    args = parser.parse_args()
    ejecutar_desde_argumentos(args)


if __name__ == "__main__":
    main()
