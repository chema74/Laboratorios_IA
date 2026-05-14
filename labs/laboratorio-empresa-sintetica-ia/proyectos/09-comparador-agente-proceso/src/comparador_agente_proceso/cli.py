"""CLI del comparador entre flujo manual, automatizado y agente simulado."""

from __future__ import annotations

import argparse

from .cargador_contexto import cargar_contexto
from .catalogo_procesos import construir_procesos_comparados
from .comparador import construir_comparaciones
from .evaluador_metricas import construir_expediente, construir_resumen
from .exportador import exportar_resultados
from .simulador_flujos import simular_resultados_flujos


def crear_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Comparador agente-proceso local")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--salida", type=str, default="datos_ejemplo/comparador_agente_proceso_demo")
    p.add_argument("--entrada-empresa", type=str, default="datos_ejemplo/empresa_sintetica_demo/empresa_sintetica.json")
    p.add_argument("--entrada-eventos", type=str, default="datos_ejemplo/eventos_negocio_demo/eventos_negocio.json")
    p.add_argument("--entrada-documentos", type=str, default="datos_ejemplo/documentos_sinteticos_demo/indice_documentos.json")
    p.add_argument("--entrada-escenarios", type=str, default="datos_ejemplo/escenarios_prueba_agentes_demo/escenarios_prueba_agentes.json")
    p.add_argument("--entrada-crisis", type=str, default="datos_ejemplo/crisis_simuladas_demo/crisis_simuladas.json")
    p.add_argument("--entrada-revisiones", type=str, default="datos_ejemplo/revision_humana_demo/revisiones_humanas.json")
    p.add_argument("--entrada-registro-decisiones", type=str, default="datos_ejemplo/revision_humana_demo/registro_decisiones.json")
    p.add_argument("--entrada-estado-operativo", type=str, default="datos_ejemplo/gemelo_digital_operativo_demo/estado_operativo.json")
    p.add_argument("--entrada-alertas", type=str, default="datos_ejemplo/gemelo_digital_operativo_demo/alertas_operativas.json")
    p.add_argument("--entrada-decisiones", type=str, default="datos_ejemplo/gemelo_digital_operativo_demo/decisiones_simuladas.json")
    p.add_argument("--entrada-inventario-privacidad", type=str, default="datos_ejemplo/privacidad_datos_sinteticos_demo/inventario_datos_sinteticos.json")
    p.add_argument("--entrada-riesgos-privacidad", type=str, default="datos_ejemplo/privacidad_datos_sinteticos_demo/riesgos_privacidad_simulados.json")
    p.add_argument("--procesos", type=int, default=7)
    return p


def ejecutar_desde_argumentos(args: argparse.Namespace) -> tuple[list[dict], dict[str, str]]:
    """
    1) Carga contexto previo o fallback.
    2) Simula métricas de los tres flujos por proceso.
    3) Construye comparación, resumen y exporta resultados.
    """
    paths = {
        "entrada_empresa": args.entrada_empresa,
        "entrada_eventos": args.entrada_eventos,
        "entrada_documentos": args.entrada_documentos,
        "entrada_escenarios": args.entrada_escenarios,
        "entrada_crisis": args.entrada_crisis,
        "entrada_revisiones": args.entrada_revisiones,
        "entrada_registro_decisiones": args.entrada_registro_decisiones,
        "entrada_estado_operativo": args.entrada_estado_operativo,
        "entrada_alertas": args.entrada_alertas,
        "entrada_decisiones": args.entrada_decisiones,
        "entrada_inventario_privacidad": args.entrada_inventario_privacidad,
        "entrada_riesgos_privacidad": args.entrada_riesgos_privacidad,
    }

    contexto = cargar_contexto(paths)
    procesos = construir_procesos_comparados(contexto, procesos=args.procesos)
    resultados = simular_resultados_flujos(procesos, seed=args.seed)
    comparaciones = construir_comparaciones(procesos, resultados)
    resumen = construir_resumen(procesos, resultados, comparaciones, paths)
    expediente = construir_expediente(procesos, resultados, comparaciones, resumen)

    rutas = exportar_resultados(procesos, resultados, comparaciones, resumen, expediente, args.salida)

    print("Comparación agente-proceso completada correctamente.")
    print(f"Procesos: {rutas['procesos_json']}")
    print(f"Comparaciones: {rutas['comparaciones_json']}")
    print(f"Resumen: {rutas['resumen_json']}")

    return procesos, rutas


def main() -> None:
    args = crear_parser().parse_args()
    ejecutar_desde_argumentos(args)


if __name__ == "__main__":
    main()
