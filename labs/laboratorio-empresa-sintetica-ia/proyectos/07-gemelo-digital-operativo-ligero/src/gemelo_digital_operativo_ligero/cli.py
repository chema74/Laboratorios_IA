"""CLI del gemelo digital operativo ligero."""

from __future__ import annotations

import argparse

from .cargador_contexto import cargar_contexto
from .evaluador_consecuencias import (
    construir_expediente_estado_operativo,
    construir_resumen_gemelo,
    generar_consecuencias_operativas,
)
from .exportador import exportar_gemelo_digital
from .simulador_estado import construir_estado_operativo


def crear_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Gemelo digital operativo ligero local")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--entrada-empresa", type=str, default="datos_ejemplo/empresa_sintetica_demo/empresa_sintetica.json")
    parser.add_argument("--entrada-eventos", type=str, default="datos_ejemplo/eventos_negocio_demo/eventos_negocio.json")
    parser.add_argument("--entrada-documentos", type=str, default="datos_ejemplo/documentos_sinteticos_demo/indice_documentos.json")
    parser.add_argument("--entrada-escenarios", type=str, default="datos_ejemplo/escenarios_prueba_agentes_demo/escenarios_prueba_agentes.json")
    parser.add_argument("--entrada-crisis", type=str, default="datos_ejemplo/crisis_simuladas_demo/crisis_simuladas.json")
    parser.add_argument("--entrada-revisiones", type=str, default="datos_ejemplo/revision_humana_demo/revisiones_humanas.json")
    parser.add_argument("--entrada-registro-decisiones", type=str, default="datos_ejemplo/revision_humana_demo/registro_decisiones.json")
    parser.add_argument("--salida", type=str, default="datos_ejemplo/gemelo_digital_operativo_demo")
    parser.add_argument("--dias", type=int, default=10)
    return parser


def ejecutar_desde_argumentos(args: argparse.Namespace) -> tuple[dict, list[dict], dict, dict[str, str]]:
    """
    1) Carga contexto consolidado de proyectos previos.
    2) Construye estado operativo, alertas y decisiones simuladas.
    3) Evalúa consecuencias y exporta artefactos finales.
    """
    contexto = cargar_contexto(
        args.entrada_empresa,
        args.entrada_eventos,
        args.entrada_documentos,
        args.entrada_escenarios,
        args.entrada_crisis,
        args.entrada_revisiones,
        args.entrada_registro_decisiones,
    )

    estado = construir_estado_operativo(contexto, seed=args.seed, dias=args.dias)
    consecuencias = generar_consecuencias_operativas(estado["alertas_operativas"], estado["decisiones_simuladas"])

    entradas = {
        "entrada_empresa": args.entrada_empresa,
        "entrada_eventos": args.entrada_eventos,
        "entrada_documentos": args.entrada_documentos,
        "entrada_escenarios": args.entrada_escenarios,
        "entrada_crisis": args.entrada_crisis,
        "entrada_revisiones": args.entrada_revisiones,
        "entrada_registro_decisiones": args.entrada_registro_decisiones,
    }
    resumen = construir_resumen_gemelo(estado, consecuencias, entradas)
    expediente = construir_expediente_estado_operativo(estado, consecuencias, resumen)
    rutas = exportar_gemelo_digital(estado, consecuencias, resumen, expediente, args.salida)

    print("Gemelo digital operativo generado correctamente.")
    print(f"Estado operativo: {rutas['estado_operativo']}")
    print(f"Resumen: {rutas['resumen_json']}")
    print(f"Expediente: {rutas['expediente_md']}")

    return estado, consecuencias, resumen, rutas


def main() -> None:
    parser = crear_parser()
    args = parser.parse_args()
    ejecutar_desde_argumentos(args)


if __name__ == "__main__":
    main()
