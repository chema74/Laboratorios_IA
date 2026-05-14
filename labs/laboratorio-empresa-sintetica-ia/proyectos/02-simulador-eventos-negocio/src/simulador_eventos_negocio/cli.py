"""CLI del simulador de eventos de negocio."""

from __future__ import annotations

import argparse
from pathlib import Path

from .cargador_empresa import cargar_empresa_sintetica
from .exportador import exportar_eventos_json_csv, exportar_resumen_json
from .simulador import construir_resumen_eventos, simular_eventos_negocio


def crear_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Simulador local de eventos de negocio")
    parser.add_argument("--seed", type=int, default=42, help="Semilla para simulación reproducible")
    parser.add_argument("--dias", type=int, default=7, help="Número de días simulados")
    parser.add_argument("--eventos-por-dia", type=int, default=8, help="Eventos aproximados por día")
    parser.add_argument(
        "--entrada-empresa",
        type=str,
        default="datos_ejemplo/empresa_sintetica_demo/empresa_sintetica.json",
        help="Ruta JSON de empresa sintética de entrada",
    )
    parser.add_argument(
        "--salida",
        type=str,
        default="datos_ejemplo/eventos_negocio_demo",
        help="Carpeta de salida de eventos y resumen",
    )
    return parser


def ejecutar_desde_argumentos(args: argparse.Namespace) -> tuple[list[dict], dict]:
    """
    1) Carga empresa de entrada (o fallback interno).
    2) Simula eventos de negocio reproducibles.
    3) Exporta eventos y resumen en JSON/CSV.
    """
    empresa = cargar_empresa_sintetica(args.entrada_empresa)
    eventos = simular_eventos_negocio(
        empresa=empresa,
        seed=args.seed,
        dias=args.dias,
        eventos_por_dia=args.eventos_por_dia,
    )
    resumen = construir_resumen_eventos(eventos)

    ruta_salida = Path(args.salida)
    ruta_json, ruta_csv = exportar_eventos_json_csv(eventos, ruta_salida)
    ruta_resumen = exportar_resumen_json(resumen, ruta_salida)

    print("Simulación completada correctamente.")
    print(f"Entrada empresa usada: {args.entrada_empresa}")
    print(f"Eventos JSON: {ruta_json}")
    print(f"Eventos CSV: {ruta_csv}")
    print(f"Resumen JSON: {ruta_resumen}")

    return eventos, resumen


def main() -> None:
    parser = crear_parser()
    args = parser.parse_args()
    ejecutar_desde_argumentos(args)


if __name__ == "__main__":
    main()
