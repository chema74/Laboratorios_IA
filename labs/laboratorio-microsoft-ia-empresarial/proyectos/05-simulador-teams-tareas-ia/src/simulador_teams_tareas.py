import argparse
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

CAMPOS_OBLIGATORIOS = [
    "id_elemento",
    "tipo_elemento",
    "canal_simulado",
    "titulo",
    "descripcion_sintetica",
    "participantes_ficticios",
    "fecha_simulada",
    "prioridad",
    "area_negocio",
    "requiere_resumen",
    "requiere_tarea",
    "requiere_seguimiento",
    "riesgo_bloqueo_simulado",
    "accion_ia_esperada",
    "responsable_ficticio",
    "limites_declarados",
    "usa_teams_real",
    "usa_planner_real",
    "usa_todo_real",
    "usa_microsoft_graph_real",
    "usa_oauth_real",
    "usa_api_externa",
    "usa_azure",
    "usa_ia_real",
    "nota_sintetica",
]


def cargar_json(ruta: Path) -> dict:
    with ruta.open("r", encoding="utf-8") as f:
        return json.load(f)


def validar_elementos(elementos: list[dict], config: dict) -> None:
    tipos = set(config["tipos_elemento_permitidos"])
    canales = set(config["canales_simulados"])
    prioridades = set(config["prioridades_permitidas"])
    areas = set(config["areas_negocio_permitidas"])
    riesgos = set(config["reglas_riesgo_bloqueo"]["niveles_permitidos"])
    for i, el in enumerate(elementos, start=1):
        faltantes = [c for c in CAMPOS_OBLIGATORIOS if c not in el]
        if faltantes:
            raise ValueError(f"Elemento {i} invalido, faltan {faltantes}")
        if el["tipo_elemento"] not in tipos:
            raise ValueError(f"Tipo no permitido: {el['id_elemento']}")
        if el["canal_simulado"] not in canales:
            raise ValueError(f"Canal no permitido: {el['id_elemento']}")
        if el["prioridad"] not in prioridades:
            raise ValueError(f"Prioridad no permitida: {el['id_elemento']}")
        if el["area_negocio"] not in areas:
            raise ValueError(f"Area no permitida: {el['id_elemento']}")
        if el["riesgo_bloqueo_simulado"] not in riesgos:
            raise ValueError(f"Riesgo no permitido: {el['id_elemento']}")
        for b in [
            "usa_teams_real",
            "usa_planner_real",
            "usa_todo_real",
            "usa_microsoft_graph_real",
            "usa_oauth_real",
            "usa_api_externa",
            "usa_azure",
            "usa_ia_real",
        ]:
            if el[b] is not False:
                raise ValueError(f"{el['id_elemento']} incumple politica en {b}")


def resumir(texto: str, max_palabras: int) -> str:
    partes = texto.split()
    return " ".join(partes[:max_palabras]) + ("..." if len(partes) > max_palabras else "")


def tarea_recomendada(el: dict) -> str:
    if not el["requiere_tarea"]:
        return "No aplica"
    return f"Crear tarea simulada para '{el['titulo']}' con responsable {el['responsable_ficticio']}."


def seguimiento_recomendado(el: dict) -> str:
    if not el["requiere_seguimiento"]:
        return "No aplica"
    return f"Programar seguimiento simulado del elemento {el['id_elemento']} en canal {el['canal_simulado']}."


def guardar_registro(teams_dir: Path, resultado: dict) -> str:
    teams_dir.mkdir(parents=True, exist_ok=True)
    ruta = teams_dir / f"{resultado['id_elemento']}.json"
    ruta.write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(ruta)


def generar_informe_md(resultados: list[dict]) -> str:
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    por_tipo = Counter(r["tipo_elemento"] for r in resultados)
    por_canal = Counter(r["canal_simulado"] for r in resultados)
    por_prioridad = Counter(r["prioridad_detectada"] for r in resultados)
    tareas = [r["id_elemento"] for r in resultados if r["tarea_recomendada_simulada"] != "No aplica"]
    segs = [r["id_elemento"] for r in resultados if r["seguimiento_recomendado_simulado"] != "No aplica"]
    riesgos = Counter(r["riesgo_bloqueo_detectado"] for r in resultados)
    md = [
        "# Informe Simulador Teams y Tareas IA (V1 Local)",
        "",
        f"Fecha de generación: {fecha}",
        "",
        "## Resumen ejecutivo",
        "Simulación local de conversaciones, reuniones y tareas con salidas sintéticas sin Microsoft real.",
        "",
        "## Total de elementos simulados",
        f"- {len(resultados)}",
        "",
        "## Distribución por tipo",
    ]
    for k in sorted(por_tipo):
        md.append(f"- {k}: {por_tipo[k]}")
    md.extend(["", "## Distribución por canal"])
    for k in sorted(por_canal):
        md.append(f"- {k}: {por_canal[k]}")
    md.extend(["", "## Distribución por prioridad"])
    for k in sorted(por_prioridad):
        md.append(f"- {k}: {por_prioridad[k]}")
    md.extend(["", "## Tareas recomendadas", "- " + ", ".join(tareas) if tareas else "- Ninguna"])
    md.extend(["", "## Seguimientos recomendados", "- " + ", ".join(segs) if segs else "- Ninguno"])
    md.extend(["", "## Riesgos de bloqueo simulados"])
    for k in sorted(riesgos):
        md.append(f"- {k}: {riesgos[k]}")
    md.extend(["", "## Ejemplos de resúmenes simulados"])
    for r in resultados[:3]:
        md.append(f"- {r['id_elemento']}: {r['resumen_simulado']}")
    md.extend(
        [
            "",
            "## Límites de la simulación",
            "- Sin Teams real.",
            "- Sin Planner real ni To Do real.",
            "- Sin Microsoft Graph API real.",
            "- Sin OAuth real.",
            "- Sin Azure obligatorio.",
            "- Sin IA real ni datos reales.",
            "",
            "## Recomendaciones siguientes",
            "- Mantener reglas de priorización y seguimiento por área.",
            "- Versionar umbrales de riesgo de bloqueo simulado.",
            "- Preparar V2 opcional con .env y fallback local.",
            "",
            "## 🪪 Licencia y Autoría",
            "Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  ",
            "© 2025 – Txema Ríos. Todos los derechos compartidos.",
            "",
        ]
    )
    return "\n".join(md)


def ejecutar(items_path: Path, config_path: Path, output_md: Path, output_json: Path, teams_dir: Path) -> dict:
    data = cargar_json(items_path)
    config = cargar_json(config_path)
    elementos = data.get("elementos", [])
    if not elementos:
        raise ValueError("No hay elementos para procesar.")
    validar_elementos(elementos, config)
    max_palabras = int(config["reglas_resumen"]["max_palabras"])
    resultados = []
    for el in elementos:
        resumen_txt = resumir(el["descripcion_sintetica"], max_palabras) if el["requiere_resumen"] else "No aplica"
        resultado = {
            "id_elemento": el["id_elemento"],
            "tipo_elemento": el["tipo_elemento"],
            "canal_simulado": el["canal_simulado"],
            "prioridad_detectada": el["prioridad"],
            "requiere_resumen": el["requiere_resumen"],
            "requiere_tarea": el["requiere_tarea"],
            "requiere_seguimiento": el["requiere_seguimiento"],
            "riesgo_bloqueo_detectado": el["riesgo_bloqueo_simulado"],
            "resumen_simulado": resumen_txt,
            "tarea_recomendada_simulada": tarea_recomendada(el),
            "seguimiento_recomendado_simulado": seguimiento_recomendado(el),
            "registro_generado": "",
            "usa_teams_real": False,
            "usa_planner_real": False,
            "usa_todo_real": False,
            "usa_microsoft_graph_real": False,
            "usa_oauth_real": False,
            "usa_api_externa": False,
            "usa_azure": False,
            "usa_ia_real": False,
        }
        resultado["registro_generado"] = guardar_registro(teams_dir, resultado)
        resultados.append(resultado)

    salida = {
        "metadata": {
            "fecha_generacion": datetime.now().isoformat(timespec="seconds"),
            "total_elementos": len(resultados),
            "nota": config.get("nota", ""),
        },
        "resumen_por_tipo": dict(Counter(r["tipo_elemento"] for r in resultados)),
        "resumen_por_canal": dict(Counter(r["canal_simulado"] for r in resultados)),
        "resumen_por_prioridad": dict(Counter(r["prioridad_detectada"] for r in resultados)),
        "resultados": resultados,
    }
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(generar_informe_md(resultados), encoding="utf-8")
    output_json.write_text(json.dumps(salida, ensure_ascii=False, indent=2), encoding="utf-8")
    return salida


def crear_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Simulador local de Teams y tareas con IA simulada.")
    p.add_argument("--items", required=True, type=Path)
    p.add_argument("--config", required=True, type=Path)
    p.add_argument("--output-md", required=True, type=Path)
    p.add_argument("--output-json", required=True, type=Path)
    p.add_argument("--teams-dir", required=True, type=Path)
    return p


def main() -> None:
    args = crear_parser().parse_args()
    ejecutar(args.items, args.config, args.output_md, args.output_json, args.teams_dir)


if __name__ == "__main__":
    main()
