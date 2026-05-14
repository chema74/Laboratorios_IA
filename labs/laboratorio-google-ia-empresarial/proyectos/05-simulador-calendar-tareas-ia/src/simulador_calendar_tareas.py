"""Simulador local de Calendar y tareas con IA simulada."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

CAMPOS = {
    "id_elemento",
    "tipo_elemento",
    "titulo",
    "descripcion_sintetica",
    "fecha_inicio_simulada",
    "fecha_fin_simulada",
    "prioridad",
    "responsable_ficticio",
    "area_negocio",
    "origen_simulado",
    "requiere_recordatorio",
    "requiere_replanificacion",
    "riesgo_retraso_simulado",
    "accion_ia_esperada",
    "limites_declarados",
    "usa_calendar_real",
    "usa_oauth_real",
    "usa_api_externa",
    "usa_cloud",
    "usa_ia_real",
    "nota_sintetica",
}


def cargar_json(ruta: Path) -> dict:
    with ruta.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def validar_elementos(elementos: list[dict], config: dict) -> None:
    prioridades = set(config["prioridades_permitidas"])
    areas = set(config["areas_negocio_permitidas"])
    tipos = {"evento", "tarea"}
    for item in elementos:
        faltan = CAMPOS.difference(item.keys())
        if faltan:
            raise ValueError(f"Elemento incompleto {item.get('id_elemento')}: {sorted(faltan)}")
        if item["prioridad"] not in prioridades:
            raise ValueError(f"Prioridad inválida: {item['prioridad']}")
        if item["area_negocio"] not in areas:
            raise ValueError(f"Área inválida: {item['area_negocio']}")
        if item["tipo_elemento"] not in tipos:
            raise ValueError(f"Tipo inválido: {item['tipo_elemento']}")


def detectar_recordatorio(item: dict, config: dict) -> bool:
    forzadas = set(config["reglas_recordatorio"]["prioridades_con_recordatorio_forzado"])
    return item["requiere_recordatorio"] or item["prioridad"] in forzadas


def detectar_replanificacion(item: dict, config: dict) -> bool:
    if item["requiere_replanificacion"]:
        return True
    texto = f"{item['titulo']} {item['descripcion_sintetica']}".lower()
    return any(k.lower() in texto for k in config["reglas_replanificacion"]["palabras_clave"])


def detectar_riesgo(item: dict) -> str:
    return item["riesgo_retraso_simulado"]


def accion_recomendada(item: dict, rec: bool, rep: bool, riesgo: str) -> str:
    if rep and riesgo == "alto":
        return "replanificar_con_prioridad"
    if rec and item["prioridad"] == "alta":
        return "recordar_y_priorizar"
    if rep:
        return "replanificar"
    return "mantener_agenda"


def guardar_registro(cal_dir: Path, registro: dict) -> str:
    cal_dir.mkdir(parents=True, exist_ok=True)
    ruta = cal_dir / f"{registro['id_elemento']}.json"
    ruta.write_text(json.dumps(registro, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(ruta)


def procesar(data: dict, config: dict, cal_dir: Path) -> list[dict]:
    elementos = data["elementos"]
    validar_elementos(elementos, config)
    salida = []
    for item in elementos:
        rec = detectar_recordatorio(item, config)
        rep = detectar_replanificacion(item, config)
        riesgo = detectar_riesgo(item)
        registro = {
            "id_elemento": item["id_elemento"],
            "tipo_elemento": item["tipo_elemento"],
            "prioridad_detectada": item["prioridad"],
            "requiere_recordatorio": rec,
            "requiere_replanificacion": rep,
            "riesgo_retraso_detectado": riesgo,
            "accion_recomendada_simulada": accion_recomendada(item, rec, rep, riesgo),
            "agenda_local": f"{item['fecha_inicio_simulada']} -> {item['fecha_fin_simulada']} | {item['titulo']}",
            "registro_generado": "",
            "usa_calendar_real": False,
            "usa_oauth_real": False,
            "usa_api_externa": False,
            "usa_cloud": False,
            "usa_ia_real": False,
        }
        registro["registro_generado"] = guardar_registro(cal_dir, registro)
        salida.append(registro)
    return salida


def resumen_global(resultados: list[dict], config: dict) -> dict:
    return {
        "fecha_generacion": datetime.now().isoformat(timespec="seconds"),
        "total_elementos": len(resultados),
        "distribucion_por_tipo": dict(Counter(x["tipo_elemento"] for x in resultados)),
        "distribucion_por_prioridad": dict(Counter(x["prioridad_detectada"] for x in resultados)),
        "distribucion_por_area": dict(Counter(x["id_elemento"].split("-")[0] for x in resultados)),
        "con_recordatorio": [x["id_elemento"] for x in resultados if x["requiere_recordatorio"]],
        "con_replanificacion": [x["id_elemento"] for x in resultados if x["requiere_replanificacion"]],
        "riesgos_retraso": dict(Counter(x["riesgo_retraso_detectado"] for x in resultados)),
        "agenda_local_simulada": [x["agenda_local"] for x in resultados],
        "nota": config["nota"],
        "resultados": resultados,
    }


def generar_md(resultado: dict, output_md: Path) -> None:
    l = [
        "# Informe de Simulación Calendar y Tareas IA",
        "",
        f"**Fecha de generación:** {resultado['fecha_generacion']}",
        "",
        "## Resumen ejecutivo",
        "Agenda y tareas sintéticas procesadas localmente sin Calendar real, OAuth real, API real ni IA real.",
        "",
        "## Total de eventos y tareas",
        f"- {resultado['total_elementos']}",
        "",
        "## Distribución por tipo",
    ]
    for k, v in resultado["distribucion_por_tipo"].items():
        l.append(f"- {k}: {v}")
    l.extend(["", "## Distribución por prioridad"])
    for k, v in resultado["distribucion_por_prioridad"].items():
        l.append(f"- {k}: {v}")
    l.extend(["", "## Elementos con recordatorio"])
    for x in resultado["con_recordatorio"]:
        l.append(f"- {x}")
    l.extend(["", "## Elementos con replanificación"])
    for x in resultado["con_replanificacion"]:
        l.append(f"- {x}")
    l.extend(["", "## Riesgos de retraso simulados"])
    for k, v in resultado["riesgos_retraso"].items():
        l.append(f"- {k}: {v}")
    l.extend(["", "## Agenda local simulada"])
    for a in resultado["agenda_local_simulada"][:10]:
        l.append(f"- {a}")
    l.extend(
        [
            "",
            "## Límites de la simulación",
            "Sin Calendar real, sin OAuth real, sin Calendar API, sin Google Cloud y sin IA real.",
            "",
            "## Recomendaciones siguientes",
            "1. Integrar reglas de conflicto horario simulado.",
            "2. Cruzar prioridades con el módulo de Gmail simulado.",
            "3. Definir V2 opcional por `.env` con fallback local.",
            "",
            "## 🪪 Licencia y Autoría",
            "Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  ",
            "© 2025 – Txema Ríos. Todos los derechos compartidos.",
        ]
    )
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text("\n".join(l), encoding="utf-8")


def args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Simulador local de calendar y tareas")
    p.add_argument("--events", required=True)
    p.add_argument("--config", required=True)
    p.add_argument("--output-md", required=True)
    p.add_argument("--output-json", required=True)
    p.add_argument("--calendar-dir", required=True)
    return p.parse_args()


def main() -> None:
    a = args()
    data = cargar_json(Path(a.events))
    config = cargar_json(Path(a.config))
    resultados = procesar(data, config, Path(a.calendar_dir))
    out = resumen_global(resultados, config)
    out_json = Path(a.output_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    generar_md(out, Path(a.output_md))


if __name__ == "__main__":
    main()
