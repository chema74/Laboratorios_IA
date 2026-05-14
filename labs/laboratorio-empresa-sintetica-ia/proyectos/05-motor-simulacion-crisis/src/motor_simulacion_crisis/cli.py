"""CLI del motor de simulación de crisis."""

from __future__ import annotations

import argparse

from .cargador_contexto import cargar_contexto
from .evaluador_impacto import construir_expediente_markdown, construir_resumen_crisis
from .exportador import exportar_resultados_crisis
from .simulador import generar_linea_tiempo, simular_crisis


def crear_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Motor local de simulación de crisis")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--entrada-empresa", type=str, default="datos_ejemplo/empresa_sintetica_demo/empresa_sintetica.json")
    parser.add_argument("--entrada-eventos", type=str, default="datos_ejemplo/eventos_negocio_demo/eventos_negocio.json")
    parser.add_argument("--entrada-documentos", type=str, default="datos_ejemplo/documentos_sinteticos_demo/indice_documentos.json")
    parser.add_argument("--entrada-escenarios", type=str, default="datos_ejemplo/escenarios_prueba_agentes_demo/escenarios_prueba_agentes.json")
    parser.add_argument("--salida", type=str, default="datos_ejemplo/crisis_simuladas_demo")
    parser.add_argument("--crisis", type=int, default=5)
    parser.add_argument("--dias", type=int, default=10)
    return parser


def ejecutar_desde_argumentos(args: argparse.Namespace) -> tuple[list[dict], list[dict], dict, dict[str, str]]:
    """
    1) Carga contexto previo o fallback.
    2) Simula crisis y línea temporal reproducible.
    3) Evalúa impacto y exporta artefactos de salida.
    """
    contexto = cargar_contexto(args.entrada_empresa, args.entrada_eventos, args.entrada_documentos, args.entrada_escenarios)
    crisis = simular_crisis(contexto, seed=args.seed, numero_crisis=args.crisis, dias=args.dias)
    linea = generar_linea_tiempo(crisis, seed=args.seed)

    entradas = {
        "entrada_empresa": args.entrada_empresa,
        "entrada_eventos": args.entrada_eventos,
        "entrada_documentos": args.entrada_documentos,
        "entrada_escenarios": args.entrada_escenarios,
    }
    resumen = construir_resumen_crisis(crisis, linea, entradas)
    expediente = construir_expediente_markdown(crisis, linea, resumen)
    rutas = exportar_resultados_crisis(crisis, linea, resumen, expediente, args.salida)

    print("Simulación de crisis completada correctamente.")
    print(f"Crisis JSON: {rutas['crisis_json']}")
    print(f"Línea tiempo JSON: {rutas['linea_json']}")
    print(f"Resumen JSON: {rutas['resumen_json']}")
    print(f"Expediente MD: {rutas['expediente_md']}")

    return crisis, linea, resumen, rutas


def main() -> None:
    parser = crear_parser()
    args = parser.parse_args()
    ejecutar_desde_argumentos(args)


if __name__ == "__main__":
    main()
