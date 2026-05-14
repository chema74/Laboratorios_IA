import argparse
import json
from collections import Counter
from datetime import datetime
from pathlib import Path


def cargar_json(ruta: Path) -> dict:
    with ruta.open("r", encoding="utf-8") as f:
        return json.load(f)


def validar_permisos(permisos: list[dict], config: dict) -> None:
    roles = set(config["roles_permitidos"])
    tipos = set(config["tipos_recurso_permitidos"])
    perms = set(config["permisos_permitidos"])
    riesgos = set(config["reglas_riesgo"]["niveles_permitidos"])
    for p in permisos:
        if p["rol_simulado"] not in roles:
            raise ValueError(f"Rol no permitido: {p['id_permiso']}")
        if p["tipo_recurso"] not in tipos:
            raise ValueError(f"Tipo recurso no permitido: {p['id_permiso']}")
        if p["permiso_asignado"] not in perms:
            raise ValueError(f"Permiso no permitido: {p['id_permiso']}")
        if p["riesgo_permiso_simulado"] not in riesgos:
            raise ValueError(f"Riesgo no permitido: {p['id_permiso']}")
        for b in ["usa_microsoft_real", "usa_microsoft_graph_real", "usa_oauth_real", "usa_api_externa", "usa_azure", "usa_ia_real"]:
            if p[b] is not False:
                raise ValueError(f"{p['id_permiso']} incumple politica en {b}")


def evaluar_permiso(p: dict, config: dict) -> dict:
    permisos_restringidos = set(config["permisos_restringidos"])
    sens_crit = set(config["reglas_revision"]["sensibilidades_criticas"])
    decision = "mantener"
    motivo = "Cumple mínimo privilegio."
    riesgo = p["riesgo_permiso_simulado"]
    excesivo = p["permiso_asignado"] in permisos_restringidos
    sensible = p["sensibilidad_recurso"] in sens_crit
    requiere_revision = p["requiere_revision"]

    if riesgo == "alto" and excesivo and sensible:
        decision = "revocar"
        motivo = "Permiso amplio en recurso sensible con riesgo alto."
    elif excesivo and (sensible or requiere_revision):
        decision = "reducir"
        motivo = "Permiso excesivo para sensibilidad declarada."
    elif requiere_revision or riesgo == "medio":
        decision = "revisar"
        motivo = "Requiere revisión por riesgo medio o marca de revisión."

    accion = config["acciones_recomendadas"][decision]
    return {
        "id_permiso": p["id_permiso"],
        "usuario_ficticio": p["usuario_ficticio"],
        "recurso_simulado": p["recurso_simulado"],
        "permiso_asignado": p["permiso_asignado"],
        "riesgo_detectado": riesgo,
        "decision_gobierno": decision,
        "motivo_decision": motivo,
        "accion_recomendada": accion,
        "registro_generado": "",
        "usa_microsoft_real": False,
        "usa_microsoft_graph_real": False,
        "usa_oauth_real": False,
        "usa_api_externa": False,
        "usa_azure": False,
        "usa_ia_real": False,
        "_tipo_recurso": p["tipo_recurso"],
        "_rol": p["rol_simulado"],
        "_requiere_revision": p["requiere_revision"],
        "_excesivo": excesivo,
    }


def guardar_registro(registry_dir: Path, resultado: dict) -> str:
    registry_dir.mkdir(parents=True, exist_ok=True)
    ruta = registry_dir / f"{resultado['id_permiso']}.json"
    copia = {k: v for k, v in resultado.items() if not k.startswith("_")}
    ruta.write_text(json.dumps(copia, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(ruta)


def generar_informe_md(resultados: list[dict]) -> str:
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    por_tipo = Counter(r["_tipo_recurso"] for r in resultados)
    por_rol = Counter(r["_rol"] for r in resultados)
    por_decision = Counter(r["decision_gobierno"] for r in resultados)
    excesivos = [r["id_permiso"] for r in resultados if r["_excesivo"]]
    revision = [r["id_permiso"] for r in resultados if r["_requiere_revision"]]
    md = [
        "# Informe Gobierno de Permisos Microsoft (Simulado)",
        "",
        f"Fecha de generación: {fecha}",
        "",
        "## Resumen ejecutivo",
        "Evaluación local de permisos simulados aplicando mínimo privilegio y decisiones defensivas.",
        "",
        "## Total de permisos evaluados",
        f"- {len(resultados)}",
        "",
        "## Distribución por tipo de recurso",
    ]
    for k in sorted(por_tipo):
        md.append(f"- {k}: {por_tipo[k]}")
    md.extend(["", "## Distribución por rol"])
    for k in sorted(por_rol):
        md.append(f"- {k}: {por_rol[k]}")
    md.extend(["", "## Permisos excesivos simulados", "- " + ", ".join(excesivos) if excesivos else "- Ninguno"])
    md.extend(["", "## Permisos que requieren revisión", "- " + ", ".join(revision) if revision else "- Ninguno"])
    md.extend(["", "## Decisiones de gobierno"])
    for k in sorted(por_decision):
        md.append(f"- {k}: {por_decision[k]}")
    md.extend(["", "## Acciones recomendadas"])
    for r in resultados[:5]:
        md.append(f"- {r['id_permiso']}: {r['accion_recomendada']}")
    md.extend(
        [
            "",
            "## Límites de la simulación",
            "- Sin Microsoft real.",
            "- Sin Microsoft Graph API real.",
            "- Sin OAuth real.",
            "- Sin Azure obligatorio.",
            "- Sin IA real ni datos reales.",
            "",
            "## Recomendaciones siguientes",
            "- Versionar reglas de mínimo privilegio por tipo de recurso.",
            "- Formalizar excepciones temporales con caducidad simulada.",
            "- Integrar trazabilidad de decisiones con el módulo 08.",
            "",
            "## 🪪 Licencia y Autoría",
            "Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  ",
            "© 2025 – Txema Ríos. Todos los derechos compartidos.",
            "",
        ]
    )
    return "\n".join(md)


def ejecutar(permissions_path: Path, config_path: Path, output_md: Path, output_json: Path, registry_dir: Path) -> dict:
    data = cargar_json(permissions_path)
    config = cargar_json(config_path)
    permisos = data.get("permisos", [])
    if not permisos:
        raise ValueError("No hay permisos para procesar.")
    validar_permisos(permisos, config)
    resultados = []
    for p in permisos:
        r = evaluar_permiso(p, config)
        r["registro_generado"] = guardar_registro(registry_dir, r)
        resultados.append(r)

    salida = {
        "metadata": {
            "fecha_generacion": datetime.now().isoformat(timespec="seconds"),
            "total_permisos": len(resultados),
            "nota": config.get("nota", ""),
        },
        "resumen_por_tipo_recurso": dict(Counter(r["_tipo_recurso"] for r in resultados)),
        "resumen_por_rol": dict(Counter(r["_rol"] for r in resultados)),
        "resumen_por_decision": dict(Counter(r["decision_gobierno"] for r in resultados)),
        "resultados": [{k: v for k, v in r.items() if not k.startswith("_")} for r in resultados],
    }
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(generar_informe_md(resultados), encoding="utf-8")
    output_json.write_text(json.dumps(salida, ensure_ascii=False, indent=2), encoding="utf-8")
    return salida


def crear_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Simulador local de gobierno de permisos Microsoft.")
    p.add_argument("--permissions", required=True, type=Path)
    p.add_argument("--config", required=True, type=Path)
    p.add_argument("--output-md", required=True, type=Path)
    p.add_argument("--output-json", required=True, type=Path)
    p.add_argument("--registry-dir", required=True, type=Path)
    return p


def main() -> None:
    args = crear_parser().parse_args()
    ejecutar(args.permissions, args.config, args.output_md, args.output_json, args.registry_dir)


if __name__ == "__main__":
    main()
