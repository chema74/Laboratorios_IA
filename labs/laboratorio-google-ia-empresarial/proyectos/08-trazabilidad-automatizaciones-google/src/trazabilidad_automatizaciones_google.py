"""Trazabilidad local de automatizaciones Google simuladas."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from datetime import datetime
from pathlib import Path


def cargar_json(ruta: Path) -> dict:
    with ruta.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def validar(autos: list[dict], c: dict) -> None:
    origenes = set(c["origenes_permitidos"])
    estados = set(c["estados_ejecucion_permitidos"])
    sens = set(c["niveles_sensibilidad"])
    for a in autos:
        if a["origen_simulado"] not in origenes or a["estado_ejecucion"] not in estados or a["sensibilidad_implicada"] not in sens:
            raise ValueError(f"Automatización inválida: {a['id_automatizacion']}")


def id_traza(a: dict, c: dict) -> str:
    fecha = datetime.now().strftime("%Y%m%d")
    return c["formato_id_traza"].format(id=a["id_automatizacion"], fecha=fecha)


def hash_simulado(a: dict) -> str:
    base = f"{a['id_automatizacion']}|{a['origen_simulado']}|{a['accion_simulada']}|{a['estado_ejecucion']}"
    return hashlib.sha256(base.encode("utf-8")).hexdigest()[:16]


def trazabilidad_suficiente(a: dict, c: dict) -> bool:
    minima = c["reglas_trazabilidad"]["min_campos"]
    campos_no_vacios = sum(1 for _, v in a.items() if str(v).strip() != "")
    evidencia_ok = a["evidencia_generada"] == c["reglas_evidencia"]["valor_positivo"]
    return campos_no_vacios >= minima and evidencia_ok


def requiere_revision(a: dict, suficiente: bool, c: dict) -> bool:
    if a["requiere_revision"]:
        return True
    if not suficiente:
        return True
    if c["reglas_revision_humana"]["sensibilidad_alta"] and a["sensibilidad_implicada"] == "alta":
        return True
    return a["estado_ejecucion"] in c["reglas_revision_humana"]["estado_critico"]


def guardar_registro(registry_dir: Path, r: dict) -> str:
    registry_dir.mkdir(parents=True, exist_ok=True)
    ruta = registry_dir / f"{r['id_automatizacion']}.json"
    ruta.write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(ruta)


def procesar(data: dict, c: dict, registry_dir: Path) -> list[dict]:
    autos = data["automatizaciones"]
    validar(autos, c)
    out = []
    for a in autos:
        suficiente = trazabilidad_suficiente(a, c)
        r = {
            "id_automatizacion": a["id_automatizacion"],
            "id_traza": id_traza(a, c),
            "hash_simulado": hash_simulado(a),
            "origen_simulado": a["origen_simulado"],
            "accion_simulada": a["accion_simulada"],
            "estado_ejecucion": a["estado_ejecucion"],
            "trazabilidad_suficiente": suficiente,
            "evidencia_generada": a["evidencia_generada"],
            "requiere_revision": requiere_revision(a, suficiente, c),
            "registro_generado": "",
            "usa_google_real": False,
            "usa_oauth_real": False,
            "usa_api_externa": False,
            "usa_cloud": False,
            "usa_ia_real": False,
        }
        r["registro_generado"] = guardar_registro(registry_dir, r)
        out.append(r)
    return out


def resumen(resultados: list[dict], c: dict) -> dict:
    return {
        "fecha_generacion": datetime.now().isoformat(timespec="seconds"),
        "total_automatizaciones": len(resultados),
        "trazas_generadas": [x["id_traza"] for x in resultados],
        "distribucion_origen": dict(Counter(x["origen_simulado"] for x in resultados)),
        "distribucion_estado": dict(Counter(x["estado_ejecucion"] for x in resultados)),
        "distribucion_sensibilidad": dict(Counter("alta" if x["requiere_revision"] else "media/baja" for x in resultados)),
        "revision_requerida": [x["id_automatizacion"] for x in resultados if x["requiere_revision"]],
        "trazabilidad_insuficiente": [x["id_automatizacion"] for x in resultados if not x["trazabilidad_suficiente"]],
        "evidencias_generadas": [x["id_automatizacion"] for x in resultados if x["evidencia_generada"] == "si"],
        "nota": c["nota"],
        "resultados": resultados,
    }


def generar_md(s: dict, out_md: Path) -> None:
    l = [
        "# Informe de Trazabilidad de Automatizaciones Google Simuladas",
        "",
        f"**Fecha de generación:** {s['fecha_generacion']}",
        "",
        "## Resumen ejecutivo",
        "Se generó trazabilidad local para automatizaciones ficticias con evaluación de suficiencia y revisión humana.",
        "",
        "## Total de automatizaciones analizadas",
        f"- {s['total_automatizaciones']}",
        "",
        "## Trazas generadas",
    ]
    for t in s["trazas_generadas"]:
        l.append(f"- {t}")
    l.extend(["", "## Distribución por origen"])
    for k, v in s["distribucion_origen"].items():
        l.append(f"- {k}: {v}")
    l.extend(["", "## Distribución por estado"])
    for k, v in s["distribucion_estado"].items():
        l.append(f"- {k}: {v}")
    l.extend(["", "## Automatizaciones con revisión requerida"])
    for x in s["revision_requerida"]:
        l.append(f"- {x}")
    l.extend(["", "## Automatizaciones con trazabilidad insuficiente"])
    for x in s["trazabilidad_insuficiente"]:
        l.append(f"- {x}")
    l.extend(["", "## Evidencias generadas"])
    for x in s["evidencias_generadas"]:
        l.append(f"- {x}")
    l.extend(
        [
            "",
            "## Límites de la simulación",
            "Sin Google real, OAuth real, APIs reales, Google Cloud ni IA real.",
            "",
            "## Recomendaciones siguientes",
            "1. Incrementar campos de evidencia por automatización.",
            "2. Alinear decisiones con módulo 07.",
            "3. Definir esquema V2 opcional por `.env` con fallback local.",
            "",
            "## 🪪 Licencia y Autoría",
            "Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  ",
            "© 2025 – Txema Ríos. Todos los derechos compartidos.",
        ]
    )
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text("\n".join(l), encoding="utf-8")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--automations", required=True)
    p.add_argument("--config", required=True)
    p.add_argument("--output-md", required=True)
    p.add_argument("--output-json", required=True)
    p.add_argument("--registry-dir", required=True)
    a = p.parse_args()
    d = cargar_json(Path(a.automations))
    c = cargar_json(Path(a.config))
    r = procesar(d, c, Path(a.registry_dir))
    s = resumen(r, c)
    out_json = Path(a.output_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(s, ensure_ascii=False, indent=2), encoding="utf-8")
    generar_md(s, Path(a.output_md))


if __name__ == "__main__":
    main()
