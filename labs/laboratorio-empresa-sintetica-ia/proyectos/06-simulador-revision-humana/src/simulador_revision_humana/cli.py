"""CLI del simulador de revisión humana."""

from __future__ import annotations

import argparse

from .cargador_contexto import cargar_contexto
from .exportador import exportar_resultados_revision
from .registro_decisiones import (
    construir_expediente_revision_markdown,
    construir_resumen_revision_humana,
    generar_registro_decisiones,
)
from .simulador import simular_revisiones_humanas


def crear_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Simulador local de revisión humana")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--entrada-eventos", type=str, default="datos_ejemplo/eventos_negocio_demo/eventos_negocio.json")
    parser.add_argument("--entrada-documentos", type=str, default="datos_ejemplo/documentos_sinteticos_demo/indice_documentos.json")
    parser.add_argument("--entrada-escenarios", type=str, default="datos_ejemplo/escenarios_prueba_agentes_demo/escenarios_prueba_agentes.json")
    parser.add_argument("--entrada-crisis", type=str, default="datos_ejemplo/crisis_simuladas_demo/crisis_simuladas.json")
    parser.add_argument("--salida", type=str, default="datos_ejemplo/revision_humana_demo")
    parser.add_argument("--revisiones", type=int, default=20)
    parser.add_argument("--porcentaje-escalado", type=int, default=25)
    return parser


def ejecutar_desde_argumentos(args: argparse.Namespace) -> tuple[list[dict], list[dict], dict, dict[str, str]]:
    """
    1) Carga contexto con fallback interno.
    2) Simula revisiones y registros con semilla reproducible.
    3) Exporta artefactos JSON/CSV/Markdown.
    """
    contexto = cargar_contexto(args.entrada_eventos, args.entrada_documentos, args.entrada_escenarios, args.entrada_crisis)

    revisiones = simular_revisiones_humanas(
        contexto=contexto,
        seed=args.seed,
        revisiones=args.revisiones,
        porcentaje_escalado=args.porcentaje_escalado,
    )
    registros = generar_registro_decisiones(revisiones, seed=args.seed)

    entradas = {
        "entrada_eventos": args.entrada_eventos,
        "entrada_documentos": args.entrada_documentos,
        "entrada_escenarios": args.entrada_escenarios,
        "entrada_crisis": args.entrada_crisis,
    }
    resumen = construir_resumen_revision_humana(revisiones, registros, entradas)
    expediente = construir_expediente_revision_markdown(revisiones, resumen)
    rutas = exportar_resultados_revision(revisiones, registros, resumen, expediente, args.salida)

    print("Simulación de revisión humana completada correctamente.")
    print(f"Revisiones JSON: {rutas['revisiones_json']}")
    print(f"Registro JSON: {rutas['registro_json']}")
    print(f"Resumen JSON: {rutas['resumen_json']}")
    print(f"Expediente MD: {rutas['expediente_md']}")

    return revisiones, registros, resumen, rutas


def main() -> None:
    parser = crear_parser()
    args = parser.parse_args()
    ejecutar_desde_argumentos(args)


if __name__ == "__main__":
    main()
