"""CLI de la fábrica de documentos sintéticos."""

from __future__ import annotations

import argparse

from .cargador_contexto import cargar_contexto
from .exportador import exportar_documentos
from .generador import construir_resumen_documentos, generar_documentos_sinteticos


def crear_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Fábrica local de documentos sintéticos")
    parser.add_argument("--seed", type=int, default=42, help="Semilla reproducible")
    parser.add_argument(
        "--entrada-empresa",
        type=str,
        default="datos_ejemplo/empresa_sintetica_demo/empresa_sintetica.json",
        help="JSON de empresa sintética",
    )
    parser.add_argument(
        "--entrada-eventos",
        type=str,
        default="datos_ejemplo/eventos_negocio_demo/eventos_negocio.json",
        help="JSON de eventos sintéticos",
    )
    parser.add_argument(
        "--salida",
        type=str,
        default="datos_ejemplo/documentos_sinteticos_demo",
        help="Carpeta de salida",
    )
    parser.add_argument("--documentos-por-tipo", type=int, default=2, help="Cantidad por tipo documental")
    return parser


def ejecutar_desde_argumentos(args: argparse.Namespace) -> tuple[list[dict], dict, dict[str, str]]:
    """
    1) Carga contexto de empresa y eventos (con fallback).
    2) Genera documentos sintéticos por tipo.
    3) Exporta Markdown e índices JSON.
    """
    contexto = cargar_contexto(args.entrada_empresa, args.entrada_eventos)
    documentos = generar_documentos_sinteticos(
        contexto=contexto,
        seed=args.seed,
        documentos_por_tipo=args.documentos_por_tipo,
    )

    entradas = {
        "entrada_empresa": args.entrada_empresa,
        "entrada_eventos": args.entrada_eventos,
    }
    resumen = construir_resumen_documentos(documentos, entradas)
    rutas = exportar_documentos(documentos, resumen, args.salida)

    print("Generación documental completada correctamente.")
    print(f"Índice: {rutas['indice_documentos']}")
    print(f"Resumen: {rutas['resumen_documentos']}")
    print(f"Total de documentos: {len(documentos)}")

    return documentos, resumen, rutas


def main() -> None:
    parser = crear_parser()
    args = parser.parse_args()
    ejecutar_desde_argumentos(args)


if __name__ == "__main__":
    main()
