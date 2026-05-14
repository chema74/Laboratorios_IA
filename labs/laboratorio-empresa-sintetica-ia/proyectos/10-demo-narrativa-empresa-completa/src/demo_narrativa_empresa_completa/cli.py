"""CLI de la demo narrativa de empresa completa."""

from __future__ import annotations

import argparse
from pathlib import Path

from .cargador_contexto import cargar_contexto
from .constructor_narrativa import construir_demo_narrativa
from .exportador import exportar_demo_narrativa
from .generador_expediente import construir_expediente_demo
from .generador_guion_demo import construir_guion_demo


def crear_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Demo narrativa local de empresa completa (proyecto 10)")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--salida", type=str, default="datos_ejemplo/demo_narrativa_empresa_completa")
    p.add_argument("--dias", type=int, default=7)

    p.add_argument("--entrada-empresa", type=str, default="datos_ejemplo/empresa_sintetica_demo/empresa_sintetica.json")
    p.add_argument("--entrada-eventos", type=str, default="datos_ejemplo/eventos_negocio_demo/eventos_negocio.json")
    p.add_argument("--entrada-resumen-eventos", type=str, default="datos_ejemplo/eventos_negocio_demo/resumen_eventos.json")
    p.add_argument("--entrada-documentos", type=str, default="datos_ejemplo/documentos_sinteticos_demo/indice_documentos.json")
    p.add_argument("--entrada-resumen-documentos", type=str, default="datos_ejemplo/documentos_sinteticos_demo/resumen_documentos.json")
    p.add_argument("--entrada-escenarios", type=str, default="datos_ejemplo/escenarios_prueba_agentes_demo/escenarios_prueba_agentes.json")
    p.add_argument("--entrada-resumen-escenarios", type=str, default="datos_ejemplo/escenarios_prueba_agentes_demo/resumen_escenarios.json")
    p.add_argument("--entrada-crisis", type=str, default="datos_ejemplo/crisis_simuladas_demo/crisis_simuladas.json")
    p.add_argument("--entrada-resumen-crisis", type=str, default="datos_ejemplo/crisis_simuladas_demo/resumen_crisis.json")
    p.add_argument("--entrada-revisiones", type=str, default="datos_ejemplo/revision_humana_demo/revisiones_humanas.json")
    p.add_argument("--entrada-registro-decisiones", type=str, default="datos_ejemplo/revision_humana_demo/registro_decisiones.json")
    p.add_argument("--entrada-resumen-revision", type=str, default="datos_ejemplo/revision_humana_demo/resumen_revision_humana.json")
    p.add_argument("--entrada-estado-operativo", type=str, default="datos_ejemplo/gemelo_digital_operativo_demo/estado_operativo.json")
    p.add_argument("--entrada-alertas", type=str, default="datos_ejemplo/gemelo_digital_operativo_demo/alertas_operativas.json")
    p.add_argument("--entrada-decisiones", type=str, default="datos_ejemplo/gemelo_digital_operativo_demo/decisiones_simuladas.json")
    p.add_argument("--entrada-resumen-gemelo", type=str, default="datos_ejemplo/gemelo_digital_operativo_demo/resumen_gemelo_digital.json")
    p.add_argument("--entrada-inventario-privacidad", type=str, default="datos_ejemplo/privacidad_datos_sinteticos_demo/inventario_datos_sinteticos.json")
    p.add_argument("--entrada-riesgos-privacidad", type=str, default="datos_ejemplo/privacidad_datos_sinteticos_demo/riesgos_privacidad_simulados.json")
    p.add_argument("--entrada-resumen-privacidad", type=str, default="datos_ejemplo/privacidad_datos_sinteticos_demo/resumen_privacidad_datos_sinteticos.json")
    p.add_argument("--entrada-procesos-comparados", type=str, default="datos_ejemplo/comparador_agente_proceso_demo/procesos_comparados.json")
    p.add_argument("--entrada-comparaciones", type=str, default="datos_ejemplo/comparador_agente_proceso_demo/comparaciones_agente_proceso.json")
    p.add_argument("--entrada-resumen-comparador", type=str, default="datos_ejemplo/comparador_agente_proceso_demo/resumen_comparador.json")
    return p


def ejecutar_desde_argumentos(args: argparse.Namespace) -> tuple[dict, dict[str, str]]:
    # 1) Definimos todas las entradas de proyectos previos.
    # 2) Cargamos contexto real o fallback para mantener reproducibilidad en tests.
    # 3) Construimos narrativa, guion y expediente; finalmente exportamos artefactos.
    entradas = {
        "entrada_empresa": args.entrada_empresa,
        "entrada_eventos": args.entrada_eventos,
        "entrada_resumen_eventos": args.entrada_resumen_eventos,
        "entrada_documentos": args.entrada_documentos,
        "entrada_resumen_documentos": args.entrada_resumen_documentos,
        "entrada_escenarios": args.entrada_escenarios,
        "entrada_resumen_escenarios": args.entrada_resumen_escenarios,
        "entrada_crisis": args.entrada_crisis,
        "entrada_resumen_crisis": args.entrada_resumen_crisis,
        "entrada_revisiones": args.entrada_revisiones,
        "entrada_registro_decisiones": args.entrada_registro_decisiones,
        "entrada_resumen_revision": args.entrada_resumen_revision,
        "entrada_estado_operativo": args.entrada_estado_operativo,
        "entrada_alertas": args.entrada_alertas,
        "entrada_decisiones": args.entrada_decisiones,
        "entrada_resumen_gemelo": args.entrada_resumen_gemelo,
        "entrada_inventario_privacidad": args.entrada_inventario_privacidad,
        "entrada_riesgos_privacidad": args.entrada_riesgos_privacidad,
        "entrada_resumen_privacidad": args.entrada_resumen_privacidad,
        "entrada_procesos_comparados": args.entrada_procesos_comparados,
        "entrada_comparaciones": args.entrada_comparaciones,
        "entrada_resumen_comparador": args.entrada_resumen_comparador,
    }
    contexto = cargar_contexto(entradas)

    narrativa = construir_demo_narrativa(
        contexto=contexto,
        seed=args.seed,
        dias=args.dias,
        base_repo=Path.cwd(),
        entradas_utilizadas=entradas,
    )
    guion_md = construir_guion_demo(narrativa)
    expediente_md = construir_expediente_demo(narrativa)

    rutas = exportar_demo_narrativa(narrativa=narrativa, guion_md=guion_md, expediente_md=expediente_md, salida=args.salida)

    print("Demo narrativa de empresa completa generada correctamente.")
    print(f"Salida principal: {rutas['demo_json']}")
    print(f"Guion de demo: {rutas['guion_md']}")
    print(f"Expediente: {rutas['expediente_md']}")
    return narrativa, rutas


def main() -> None:
    args = crear_parser().parse_args()
    ejecutar_desde_argumentos(args)


if __name__ == "__main__":
    main()

