"""CLI del laboratorio de privacidad con datos sintéticos."""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import date

from .anonimizador_demo import construir_dataset_anonimizado_demo
from .cargador_contexto import cargar_contexto
from .clasificador_sensibilidad import construir_clasificacion_sensibilidad, construir_inventario_datos
from .evaluador_riesgos import construir_riesgos_privacidad_simulados
from .exportador import exportar_resultados
from .matriz_permisos import construir_matriz_permisos_simulados
from .minimizador_datos import construir_dataset_minimizado


def _resumen(inventario: list[dict], riesgos: list[dict], matriz: list[dict], entradas: dict[str, str]) -> dict:
    niveles = Counter(d["nivel_sensibilidad_ficticia"] for d in inventario)
    riesgos_sev = Counter(r["severidad"] for r in riesgos)
    permisos_rol = Counter(m["rol"] for m in matriz)

    return {
        "fecha_generacion": date.today().isoformat(),
        "total_datos_inventariados": len(inventario),
        "datos_por_nivel_sensibilidad": dict(niveles),
        "datos_que_requieren_minimizacion": sum(1 for d in inventario if d["requiere_minimizacion"]),
        "datos_que_requieren_anonimizacion": sum(1 for d in inventario if d["requiere_anonimizacion"]),
        "datos_que_requieren_revision_humana": sum(1 for d in inventario if d["requiere_revision_humana"]),
        "riesgos_por_severidad": dict(riesgos_sev),
        "permisos_por_rol": dict(permisos_rol),
        "entradas_utilizadas": entradas,
        "advertencia_sobre_datos_sinteticos": "Análisis sobre datos sintéticos. No usar como evidencia real.",
        "advertencia_sobre_no_auditoria_legal": "No constituye auditoría legal real ni evaluación de cumplimiento real.",
        "advertencia_sobre_anonimizacion_demostrativa": "La anonimización aplicada es demostrativa y no certificada.",
    }


def _expediente(inventario: list[dict], clasificacion: list[dict], matriz: list[dict], riesgos: list[dict], resumen: dict) -> str:
    inv = "\n".join([f"- {d['id_dato']} | {d['origen']} | {d['campo']} | {d['nivel_sensibilidad_ficticia']}" for d in inventario[:20]])
    cls = "\n".join([f"- {c['origen']} | {c['tipo_entidad']} | {c['nivel_sensibilidad_ficticia']} | total={c['total']}" for c in clasificacion[:15]])
    mat = "\n".join([f"- {m['rol']} | {m['tipo_entidad']} | {m['nivel_acceso']}" for m in matriz[:20]])
    rsk = "\n".join([f"- {r['id_riesgo']} | {r['tipo_riesgo']} | {r['severidad']} | {r['estado_riesgo']}" for r in riesgos])

    return (
        "# Expediente de Privacidad con Datos Sintéticos\n\n"
        "**Aviso:** Simulación sintética para portfolio técnico. No es auditoría legal real.\n\n"
        "## Resumen ejecutivo ficticio\n"
        f"Inventario total: {resumen['total_datos_inventariados']} datos; riesgos simulados: {sum(resumen['riesgos_por_severidad'].values())}.\n\n"
        "## Inventario resumido de datos\n"
        f"{inv}\n\n"
        "## Clasificación de sensibilidad ficticia\n"
        f"{cls}\n\n"
        "## Matriz de permisos simulados\n"
        f"{mat}\n\n"
        "## Riesgos de privacidad simulados\n"
        f"{rsk}\n\n"
        "## Recomendaciones simuladas\n"
        "- minimizar_campos\n- restringir_acceso\n- anonimizar_identificadores\n- escalar_a_responsable_privacidad\n\n"
        "## Límites de uso\n"
        "- No usar como auditoría legal real.\n"
        "- No usar como cumplimiento real.\n"
        "- No usar como anonimización certificada.\n\n"
        "## Nota final\n"
        "No existe auditoría legal real, cumplimiento real ni anonimización certificada en este expediente.\n"
    )


def crear_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Laboratorio de privacidad con datos sintéticos")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--salida", type=str, default="datos_ejemplo/privacidad_datos_sinteticos_demo")
    parser.add_argument("--entrada-empresa", type=str, default="datos_ejemplo/empresa_sintetica_demo/empresa_sintetica.json")
    parser.add_argument("--entrada-eventos", type=str, default="datos_ejemplo/eventos_negocio_demo/eventos_negocio.json")
    parser.add_argument("--entrada-documentos", type=str, default="datos_ejemplo/documentos_sinteticos_demo/indice_documentos.json")
    parser.add_argument("--entrada-escenarios", type=str, default="datos_ejemplo/escenarios_prueba_agentes_demo/escenarios_prueba_agentes.json")
    parser.add_argument("--entrada-crisis", type=str, default="datos_ejemplo/crisis_simuladas_demo/crisis_simuladas.json")
    parser.add_argument("--entrada-revisiones", type=str, default="datos_ejemplo/revision_humana_demo/revisiones_humanas.json")
    parser.add_argument("--entrada-registro-decisiones", type=str, default="datos_ejemplo/revision_humana_demo/registro_decisiones.json")
    parser.add_argument("--entrada-estado-operativo", type=str, default="datos_ejemplo/gemelo_digital_operativo_demo/estado_operativo.json")
    parser.add_argument("--entrada-alertas", type=str, default="datos_ejemplo/gemelo_digital_operativo_demo/alertas_operativas.json")
    parser.add_argument("--entrada-decisiones", type=str, default="datos_ejemplo/gemelo_digital_operativo_demo/decisiones_simuladas.json")
    parser.add_argument("--max-datos", type=int, default=80)
    return parser


def ejecutar_desde_argumentos(args: argparse.Namespace) -> tuple[list[dict], dict[str, str]]:
    """
    1) Carga contexto y construye inventario/clasificación.
    2) Genera permisos, minimización, anonimización demo y riesgos.
    3) Exporta resultados JSON/CSV/Markdown.
    """
    contexto = cargar_contexto(
        args.entrada_empresa,
        args.entrada_eventos,
        args.entrada_documentos,
        args.entrada_escenarios,
        args.entrada_crisis,
        args.entrada_revisiones,
        args.entrada_registro_decisiones,
        args.entrada_estado_operativo,
        args.entrada_alertas,
        args.entrada_decisiones,
    )

    inventario = construir_inventario_datos(contexto, max_datos=args.max_datos)
    clasificacion = construir_clasificacion_sensibilidad(inventario)
    matriz = construir_matriz_permisos_simulados(inventario)
    minimizado = construir_dataset_minimizado(inventario)
    anonimizado = construir_dataset_anonimizado_demo(minimizado, seed=args.seed)
    riesgos = construir_riesgos_privacidad_simulados(inventario, matriz, contexto)

    entradas = {
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
    }
    resumen = _resumen(inventario, riesgos, matriz, entradas)
    expediente = _expediente(inventario, clasificacion, matriz, riesgos, resumen)

    rutas = exportar_resultados(
        inventario,
        clasificacion,
        matriz,
        minimizado,
        anonimizado,
        riesgos,
        resumen,
        expediente,
        args.salida,
    )

    print("Laboratorio de privacidad generado correctamente.")
    print(f"Inventario: {rutas['inventario_json']}")
    print(f"Resumen: {rutas['resumen_json']}")
    print(f"Expediente: {rutas['expediente_md']}")

    return inventario, rutas


def main() -> None:
    parser = crear_parser()
    args = parser.parse_args()
    ejecutar_desde_argumentos(args)


if __name__ == "__main__":
    main()
