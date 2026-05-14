"""CLI del generador de escenarios de prueba para agentes."""

from __future__ import annotations

import argparse

from .cargador_contexto import cargar_contexto
from .exportador import exportar_escenarios
from .generador import construir_resumen_escenarios, generar_escenarios


def crear_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generador local de escenarios de prueba para agentes")
    parser.add_argument("--seed", type=int, default=42, help="Semilla para reproducibilidad")
    parser.add_argument("--entrada-empresa", type=str, default="datos_ejemplo/empresa_sintetica_demo/empresa_sintetica.json")
    parser.add_argument("--entrada-eventos", type=str, default="datos_ejemplo/eventos_negocio_demo/eventos_negocio.json")
    parser.add_argument("--entrada-documentos", type=str, default="datos_ejemplo/documentos_sinteticos_demo/indice_documentos.json")
    parser.add_argument("--salida", type=str, default="datos_ejemplo/escenarios_prueba_agentes_demo")
    parser.add_argument("--escenarios-por-tipo", type=int, default=2)
    return parser


def ejecutar_desde_argumentos(args: argparse.Namespace) -> tuple[list[dict], dict, dict[str, str]]:
    """
    1) Carga contexto desde artefactos previos con fallback.
    2) Genera escenarios por tipo con semilla fija.
    3) Exporta artefactos para evaluación futura.
    """
    contexto = cargar_contexto(args.entrada_empresa, args.entrada_eventos, args.entrada_documentos)
    escenarios = generar_escenarios(contexto, seed=args.seed, escenarios_por_tipo=args.escenarios_por_tipo)

    entradas = {
        "entrada_empresa": args.entrada_empresa,
        "entrada_eventos": args.entrada_eventos,
        "entrada_documentos": args.entrada_documentos,
    }
    resumen = construir_resumen_escenarios(escenarios, entradas)
    rutas = exportar_escenarios(escenarios, resumen, args.salida)

    print("Generación de escenarios completada correctamente.")
    print(f"Escenarios JSON: {rutas['escenarios_json']}")
    print(f"Escenarios CSV: {rutas['escenarios_csv']}")
    print(f"Resumen JSON: {rutas['resumen_json']}")
    print(f"Markdown: {rutas['markdown_dir']}")

    return escenarios, resumen, rutas


def main() -> None:
    parser = crear_parser()
    args = parser.parse_args()
    ejecutar_desde_argumentos(args)


if __name__ == "__main__":
    main()
