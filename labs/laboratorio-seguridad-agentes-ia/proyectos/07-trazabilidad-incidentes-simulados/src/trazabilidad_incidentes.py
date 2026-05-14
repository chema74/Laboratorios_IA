from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any


def cargar_json(r: Path) -> Any:
    with r.open("r", encoding="utf-8") as f:
        return json.load(f)


def id_evidencia(inc: dict[str, Any], fmt: str) -> str:
    fecha = inc["fecha_incidente"].replace("-", "")
    return fmt.replace("{id_incidente}", inc["id_incidente"]).replace("{fecha}", fecha)


def hash_incidente(inc: dict[str, Any]) -> str:
    base = f"{inc['id_incidente']}|{inc['tipo_incidente']}|{inc['severidad_simulada']}|{inc['estado_incidente']}"
    return hashlib.sha256(base.encode("utf-8")).hexdigest()[:16]


def procesar(incs: list[dict[str, Any]], cfg: dict[str, Any], reg_dir: Path) -> dict[str, Any]:
    reg_dir.mkdir(parents=True, exist_ok=True)
    out = []
    errores = []
    for i in incs:
        bad = []
        if i.get("tipo_incidente") not in cfg["tipos_incidente_permitidos"]:
            bad.append("tipo no permitido")
        if i.get("severidad_simulada") not in cfg["severidades_permitidas"]:
            bad.append("severidad no permitida")
        if i.get("estado_incidente") not in cfg["estados_incidente_permitidos"]:
            bad.append("estado no permitido")
        for k in ("usa_datos_reales", "usa_ia_real", "usa_api_externa", "usa_cloud"):
            if i.get(k) is not False:
                bad.append(f"{k} debe ser false")
        if bad:
            errores.append(f"{i.get('id_incidente','SIN_ID')}: " + " | ".join(bad))
            continue
        evid = id_evidencia(i, cfg["formato_id_evidencia"])
        h = hash_incidente(i)
        suficientes = len(i.get("controles_aplicados", [])) >= cfg["reglas_trazabilidad"]["min_controles"]
        traz = bool(i.get("politica_relacionada") and i.get("evidencia_requerida") and i.get("responsable_simulado") and suficientes)
        r = {
            "id_incidente": i["id_incidente"],
            "id_evidencia": evid,
            "hash_simulado": h,
            "tipo_incidente": i["tipo_incidente"],
            "severidad_simulada": i["severidad_simulada"],
            "estado_incidente": i["estado_incidente"],
            "controles_aplicados": i["controles_aplicados"],
            "trazabilidad_completa": traz,
            "controles_suficientes": suficientes,
            "recomendacion_defensiva": "Reforzar controles y trazabilidad en incidentes abiertos.",
            "usa_datos_reales": False,
            "usa_ia_real": False,
            "usa_api_externa": False,
            "usa_cloud": False,
        }
        (reg_dir / f"{i['id_incidente']}.json").write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")
        out.append(r)
    return {
        "fecha_generacion": datetime.now().isoformat(timespec="seconds"),
        "total_incidentes_simulados": len(out),
        "errores_validacion": errores,
        "distribucion_por_tipo": dict(Counter(x["tipo_incidente"] for x in out)),
        "distribucion_por_severidad": dict(Counter(x["severidad_simulada"] for x in out)),
        "distribucion_por_estado": dict(Counter(x["estado_incidente"] for x in out)),
        "incidentes_trazabilidad_debil": [x for x in out if not x["trazabilidad_completa"]],
        "incidentes_sin_controles_suficientes": [x for x in out if not x["controles_suficientes"]],
        "evidencias_generadas": [x["id_evidencia"] for x in out],
        "resultados": out,
    }


def md(res: dict[str, Any]) -> str:
    lines = [
        "# Informe de Trazabilidad de Incidentes Simulados",
        "",
        f"Fecha de generación: {res['fecha_generacion']}",
        "",
        "## Resumen ejecutivo",
        "Registro local de incidentes defensivos simulados con evidencias y trazabilidad.",
        "",
        "## Total de incidentes simulados",
        str(res["total_incidentes_simulados"]),
        "",
        "## Distribución por tipo",
    ]
    lines += [f"- {k}: {v}" for k, v in res["distribucion_por_tipo"].items()]
    lines += ["", "## Distribución por severidad"]
    lines += [f"- {k}: {v}" for k, v in res["distribucion_por_severidad"].items()]
    lines += ["", "## Distribución por estado"]
    lines += [f"- {k}: {v}" for k, v in res["distribucion_por_estado"].items()]
    lines += ["", "## Incidentes con trazabilidad débil"]
    lines += [f"- {x['id_incidente']}" for x in res["incidentes_trazabilidad_debil"]] or ["- Ninguno"]
    lines += ["", "## Incidentes sin controles suficientes"]
    lines += [f"- {x['id_incidente']}" for x in res["incidentes_sin_controles_suficientes"]] or ["- Ninguno"]
    lines += ["", "## Evidencias generadas"]
    lines += [f"- {x}" for x in res["evidencias_generadas"]]
    lines += [
        "",
        "## Lectura técnica defensiva",
        "La trazabilidad permite auditar decisiones y priorizar mitigaciones sobre incidentes recurrentes.",
        "",
        "## Límites de la trazabilidad",
        "Solo escenarios sintéticos, sin datos reales ni servicios externos.",
        "",
        "## Recomendaciones siguientes",
        "1. Exigir controles mínimos por incidente.",
        "2. Cerrar incidentes abiertos con evidencia completa.",
        "3. Integrar tendencias con la matriz de riesgo.",
        "",
        "## 🪪 Licencia y Autoría",
        "Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  ",
        "© 2025 – Txema Ríos. Todos los derechos compartidos.",
    ]
    return "\n".join(lines) + "\n"


def ejecutar(inc: Path, cfg: Path, out_md: Path, out_json: Path, reg_dir: Path) -> dict[str, Any]:
    res = procesar(cargar_json(inc), cargar_json(cfg), reg_dir)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(md(res), encoding="utf-8")
    out_json.write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
    return res


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--incidents", required=True, type=Path)
    p.add_argument("--config", required=True, type=Path)
    p.add_argument("--output-md", required=True, type=Path)
    p.add_argument("--output-json", required=True, type=Path)
    p.add_argument("--registry-dir", required=True, type=Path)
    a = p.parse_args()
    r = ejecutar(a.incidents, a.config, a.output_md, a.output_json, a.registry_dir)
    print(f"Trazabilidad completada. Incidentes válidos: {r['total_incidentes_simulados']}")


if __name__ == "__main__":
    main()
