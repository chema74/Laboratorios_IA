"""Gobierno local de permisos Google simulado."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime
from pathlib import Path


def cargar_json(ruta: Path) -> dict:
    with ruta.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def validar(permisos: list[dict], c: dict) -> None:
    roles = set(c["roles_permitidos"])
    tipos = set(c["tipos_recurso_permitidos"])
    perms = set(c["permisos_permitidos"])
    for p in permisos:
        if p["rol_simulado"] not in roles or p["tipo_recurso"] not in tipos or p["permiso_asignado"] not in perms:
            raise ValueError(f"Permiso inválido: {p['id_permiso']}")


def decidir(p: dict, c: dict) -> tuple[str, str, str, str]:
    riesgo = p["riesgo_permiso_simulado"]
    restringidos = set(c["permisos_restringidos"])
    min_priv = c["reglas_minimo_privilegio"].get(p["rol_simulado"], [])
    excesivo = p["permiso_asignado"] in restringidos or (min_priv and p["permiso_asignado"] not in min_priv)
    sensible_amplio = p["sensibilidad_recurso"] == "alta" and p["permiso_asignado"] in {"edicion", "propietario_simulado", "ejecucion_simulada"}
    requiere_rev = p["requiere_revision"] or riesgo in c["reglas_revision"]["riesgos_revision"] or p["estado_permiso"] in c["reglas_revision"]["estados_revision"]
    if p["estado_permiso"] == "pendiente_revision" and excesivo:
        return riesgo, "revocar", "Permiso excesivo en estado pendiente de revisión", c["acciones_recomendadas"]["revocar"]
    if excesivo or sensible_amplio:
        return riesgo, "reducir", "Incumple mínimo privilegio o afecta recurso sensible", c["acciones_recomendadas"]["reducir"]
    if requiere_rev:
        return riesgo, "revisar", "Marcado para revisión de gobierno", c["acciones_recomendadas"]["revisar"]
    return riesgo, "mantener", "Permiso acorde a reglas simuladas", c["acciones_recomendadas"]["mantener"]


def guardar_registro(registry_dir: Path, r: dict) -> str:
    registry_dir.mkdir(parents=True, exist_ok=True)
    ruta = registry_dir / f"{r['id_permiso']}.json"
    ruta.write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(ruta)


def procesar(data: dict, c: dict, registry_dir: Path) -> list[dict]:
    permisos = data["permisos"]
    validar(permisos, c)
    out = []
    for p in permisos:
        riesgo, dec, motivo, accion = decidir(p, c)
        r = {
            "id_permiso": p["id_permiso"],
            "usuario_ficticio": p["usuario_ficticio"],
            "recurso_simulado": p["recurso_simulado"],
            "permiso_asignado": p["permiso_asignado"],
            "rol_simulado": p["rol_simulado"],
            "tipo_recurso": p["tipo_recurso"],
            "riesgo_detectado": riesgo,
            "decision_gobierno": dec,
            "motivo_decision": motivo,
            "accion_recomendada": accion,
            "requiere_revision": p["requiere_revision"],
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
        "total_permisos": len(resultados),
        "distribucion_tipo_recurso": dict(Counter(x["tipo_recurso"] for x in resultados)),
        "distribucion_rol": dict(Counter(x["rol_simulado"] for x in resultados)),
        "distribucion_decision": dict(Counter(x["decision_gobierno"] for x in resultados)),
        "permisos_excesivos_simulados": [x["id_permiso"] for x in resultados if x["decision_gobierno"] in {"reducir", "revocar"}],
        "permisos_revision": [x["id_permiso"] for x in resultados if x["decision_gobierno"] == "revisar" or x["requiere_revision"]],
        "acciones_recomendadas": list(c["acciones_recomendadas"].values()),
        "nota": c["nota"],
        "resultados": resultados,
    }


def generar_md(s: dict, out_md: Path) -> None:
    l = [
        "# Informe de Gobierno de Permisos Google Simulado",
        "",
        f"**Fecha de generación:** {s['fecha_generacion']}",
        "",
        "## Resumen ejecutivo",
        "Evaluación de permisos ficticios aplicando mínimo privilegio y decisiones defensivas locales.",
        "",
        "## Total de permisos evaluados",
        f"- {s['total_permisos']}",
        "",
        "## Distribución por tipo de recurso",
    ]
    for k, v in s["distribucion_tipo_recurso"].items():
        l.append(f"- {k}: {v}")
    l.extend(["", "## Distribución por rol"])
    for k, v in s["distribucion_rol"].items():
        l.append(f"- {k}: {v}")
    l.extend(["", "## Permisos excesivos simulados"])
    for x in s["permisos_excesivos_simulados"]:
        l.append(f"- {x}")
    l.extend(["", "## Permisos que requieren revisión"])
    for x in s["permisos_revision"]:
        l.append(f"- {x}")
    l.extend(["", "## Decisiones de gobierno"])
    for k, v in s["distribucion_decision"].items():
        l.append(f"- {k}: {v}")
    l.extend(["", "## Acciones recomendadas"])
    for a in s["acciones_recomendadas"]:
        l.append(f"- {a}")
    l.extend(
        [
            "",
            "## Límites de la simulación",
            "Sin Google real, OAuth real, APIs externas, Google Cloud ni IA real.",
            "",
            "## Recomendaciones siguientes",
            "1. Refinar reglas por combinación rol-recurso.",
            "2. Unificar métricas con módulo de trazabilidad.",
            "3. Definir V2 opcional por `.env` con fallback local.",
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
    p.add_argument("--permissions", required=True)
    p.add_argument("--config", required=True)
    p.add_argument("--output-md", required=True)
    p.add_argument("--output-json", required=True)
    p.add_argument("--registry-dir", required=True)
    a = p.parse_args()
    d = cargar_json(Path(a.permissions))
    c = cargar_json(Path(a.config))
    r = procesar(d, c, Path(a.registry_dir))
    s = resumen(r, c)
    out_json = Path(a.output_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(s, ensure_ascii=False, indent=2), encoding="utf-8")
    generar_md(s, Path(a.output_md))


if __name__ == "__main__":
    main()
