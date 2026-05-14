import argparse
import hashlib
import json
from collections import Counter
from datetime import datetime
from pathlib import Path


def cargar_json(ruta: Path) -> dict:
    with ruta.open("r", encoding="utf-8") as f:
        return json.load(f)


def validar_automatizaciones(autos: list[dict], config: dict) -> None:
    origenes = set(config["origenes_permitidos"])
    estados = set(config["estados_ejecucion_permitidos"])
    sensibilidades = set(config["niveles_sensibilidad"])
    for a in autos:
        if a["origen_simulado"] not in origenes:
            raise ValueError(f"Origen no permitido: {a['id_automatizacion']}")
        if a["estado_ejecucion"] not in estados:
            raise ValueError(f"Estado no permitido: {a['id_automatizacion']}")
        if a["sensibilidad_implicada"] not in sensibilidades:
            raise ValueError(f"Sensibilidad no permitida: {a['id_automatizacion']}")
        for b in ["usa_microsoft_real", "usa_microsoft_graph_real", "usa_oauth_real", "usa_api_externa", "usa_azure", "usa_ia_real"]:
            if a[b] is not False:
                raise ValueError(f"{a['id_automatizacion']} incumple politica en {b}")


def hash_automatizacion(a: dict) -> str:
    base = f"{a['id_automatizacion']}|{a['nombre_automatizacion']}|{a['origen_simulado']}|{a['accion_simulada']}"
    return hashlib.sha256(base.encode("utf-8")).hexdigest()


def generar_id_traza(id_auto: str, h: str, formato: str) -> str:
    return formato.replace("{id}", id_auto).replace("{hash8}", h[:8])


def evaluar_trazabilidad(a: dict, config: dict) -> tuple[bool, bool]:
    sens_crit = set(config["reglas_revision_humana"]["sensibilidades_criticas"])
    traz_ok = bool(a["trazabilidad_requerida"] and a["evidencia_generada"])
    rev = bool(a["requiere_revision"] or a["sensibilidad_implicada"] in sens_crit or not traz_ok)
    return traz_ok, rev


def guardar_registro(registry_dir: Path, resultado: dict) -> str:
    registry_dir.mkdir(parents=True, exist_ok=True)
    ruta = registry_dir / f"{resultado['id_automatizacion']}.json"
    copia = {k: v for k, v in resultado.items() if not k.startswith("_")}
    ruta.write_text(json.dumps(copia, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(ruta)


def generar_informe_md(resultados: list[dict]) -> str:
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    por_origen = Counter(r["origen_simulado"] for r in resultados)
    por_estado = Counter(r["estado_ejecucion"] for r in resultados)
    por_sens = Counter(r["_sensibilidad"] for r in resultados)
    revisiones = [r["id_automatizacion"] for r in resultados if r["requiere_revision"]]
    insuf = [r["id_automatizacion"] for r in resultados if not r["trazabilidad_suficiente"]]
    evidencias = [r["id_automatizacion"] for r in resultados if r["evidencia_generada"]]
    md = [
        "# Informe Trazabilidad de Automatizaciones Microsoft (Simulado)",
        "",
        f"Fecha de generación: {fecha}",
        "",
        "## Resumen ejecutivo",
        "Registro local de trazas, hash y evidencia para automatizaciones ficticias del ecosistema Microsoft.",
        "",
        "## Total de automatizaciones analizadas",
        f"- {len(resultados)}",
        "",
        "## Trazas generadas",
        f"- {len(resultados)}",
        "",
        "## Distribución por origen",
    ]
    for k in sorted(por_origen):
        md.append(f"- {k}: {por_origen[k]}")
    md.extend(["", "## Distribución por estado"])
    for k in sorted(por_estado):
        md.append(f"- {k}: {por_estado[k]}")
    md.extend(["", "## Automatizaciones con revisión requerida", "- " + ", ".join(revisiones) if revisiones else "- Ninguna"])
    md.extend(["", "## Automatizaciones con trazabilidad insuficiente", "- " + ", ".join(insuf) if insuf else "- Ninguna"])
    md.extend(["", "## Evidencias generadas", "- " + ", ".join(evidencias) if evidencias else "- Ninguna"])
    md.extend(
        [
            "",
            "## Límites de la simulación",
            "- Sin Microsoft real.",
            "- Sin Microsoft Graph API real.",
            "- Sin OAuth real.",
            "- Sin Azure obligatorio.",
            "- Sin IA real y sin datos reales.",
            "",
            "## Recomendaciones siguientes",
            "- Definir umbrales de trazabilidad por criticidad.",
            "- Aumentar validaciones de evidencia para estados de error.",
            "- Integrar decisiones de gobierno del módulo 07.",
            "",
            "## 🪪 Licencia y Autoría",
            "Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  ",
            "© 2025 – Txema Ríos. Todos los derechos compartidos.",
            "",
        ]
    )
    return "\n".join(md)


def ejecutar(automations_path: Path, config_path: Path, output_md: Path, output_json: Path, registry_dir: Path) -> dict:
    data = cargar_json(automations_path)
    config = cargar_json(config_path)
    autos = data.get("automatizaciones", [])
    if not autos:
        raise ValueError("No hay automatizaciones para procesar.")
    validar_automatizaciones(autos, config)
    resultados = []
    for a in autos:
        h = hash_automatizacion(a)
        id_traza = generar_id_traza(a["id_automatizacion"], h, config["formato_id_traza"])
        traz_ok, rev = evaluar_trazabilidad(a, config)
        r = {
            "id_automatizacion": a["id_automatizacion"],
            "id_traza": id_traza,
            "hash_simulado": h,
            "origen_simulado": a["origen_simulado"],
            "accion_simulada": a["accion_simulada"],
            "estado_ejecucion": a["estado_ejecucion"],
            "trazabilidad_suficiente": traz_ok,
            "evidencia_generada": a["evidencia_generada"],
            "requiere_revision": rev,
            "registro_generado": "",
            "usa_microsoft_real": False,
            "usa_microsoft_graph_real": False,
            "usa_oauth_real": False,
            "usa_api_externa": False,
            "usa_azure": False,
            "usa_ia_real": False,
            "_sensibilidad": a["sensibilidad_implicada"],
        }
        r["registro_generado"] = guardar_registro(registry_dir, r)
        resultados.append(r)

    salida = {
        "metadata": {
            "fecha_generacion": datetime.now().isoformat(timespec="seconds"),
            "total_automatizaciones": len(resultados),
            "nota": config.get("nota", ""),
        },
        "resumen_por_origen": dict(Counter(r["origen_simulado"] for r in resultados)),
        "resumen_por_estado": dict(Counter(r["estado_ejecucion"] for r in resultados)),
        "resumen_por_sensibilidad": dict(Counter(r["_sensibilidad"] for r in resultados)),
        "resultados": [{k: v for k, v in r.items() if not k.startswith("_")} for r in resultados],
    }
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(generar_informe_md(resultados), encoding="utf-8")
    output_json.write_text(json.dumps(salida, ensure_ascii=False, indent=2), encoding="utf-8")
    return salida


def crear_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Trazabilidad local de automatizaciones Microsoft simuladas.")
    p.add_argument("--automations", required=True, type=Path)
    p.add_argument("--config", required=True, type=Path)
    p.add_argument("--output-md", required=True, type=Path)
    p.add_argument("--output-json", required=True, type=Path)
    p.add_argument("--registry-dir", required=True, type=Path)
    return p


def main() -> None:
    args = crear_parser().parse_args()
    ejecutar(args.automations, args.config, args.output_md, args.output_json, args.registry_dir)


if __name__ == "__main__":
    main()
