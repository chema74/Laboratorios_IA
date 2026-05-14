from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any


def cargar_json(ruta: Path) -> Any:
    with ruta.open("r", encoding="utf-8") as f:
        return json.load(f)


def validar_estructura(s: dict[str, Any]) -> list[str]:
    campos = [
        "id_solicitud", "agente_simulado", "herramienta_simulada", "accion_solicitada",
        "contexto_sintetico", "nivel_sensibilidad_contexto", "justificacion_solicitud",
        "requiere_revision_humana", "resultado_esperado_defensivo", "limites_declarados",
        "usa_herramienta_real", "ejecuta_comando_real", "usa_datos_reales", "usa_ia_real",
        "usa_api_externa", "usa_cloud", "nota_sintetica",
    ]
    return [f"Falta campo obligatorio: {c}" for c in campos if c not in s]


def decidir(s: dict[str, Any], cfg: dict[str, Any]) -> tuple[str, str, bool, list[str]]:
    controles: list[str] = []
    herramienta = s["herramienta_simulada"]
    accion = s["accion_solicitada"]
    sens = s["nivel_sensibilidad_contexto"]
    if herramienta in cfg["herramientas_restringidas"] or accion in cfg["acciones_bloqueadas"]:
        controles.extend(["bloqueo_herramienta_restringida", "bloqueo_accion_sensible"])
        return "bloquear", "Herramienta o acción restringida por política defensiva.", True, controles
    if sens == "alto" or s.get("requiere_revision_humana"):
        controles.extend(["revision_humana_obligatoria", "trazabilidad_registro"])
        return "revisar", "Contexto de alta sensibilidad o revisión explícita.", True, controles
    if herramienta in cfg["herramientas_permitidas"] and accion in cfg["acciones_permitidas"]:
        controles.extend(["lista_permitidos", "trazabilidad_registro"])
        return "permitir", "Herramienta y acción permitidas en contexto controlado.", False, controles
    controles.extend(["revision_humana_obligatoria"])
    return "revisar", "Caso no categorizado, se deriva a revisión defensiva.", True, controles


def procesar(solicitudes: list[dict[str, Any]], cfg: dict[str, Any], reg_dir: Path) -> dict[str, Any]:
    errores: list[str] = []
    resultados: list[dict[str, Any]] = []
    reg_dir.mkdir(parents=True, exist_ok=True)
    for s in solicitudes:
        err = validar_estructura(s)
        if s.get("herramienta_simulada") not in (cfg["herramientas_permitidas"] + cfg["herramientas_restringidas"]):
            err.append("herramienta_simulada fuera de catálogo")
        if s.get("nivel_sensibilidad_contexto") not in cfg["niveles_sensibilidad"]:
            err.append("nivel_sensibilidad_contexto inválido")
        for k in ("usa_herramienta_real", "ejecuta_comando_real", "usa_datos_reales", "usa_ia_real", "usa_api_externa", "usa_cloud"):
            if s.get(k) is not False:
                err.append(f"{k} debe ser false")
        if err:
            errores.append(f"{s.get('id_solicitud','SIN_ID')}: " + " | ".join(err))
            continue
        decision, motivo, rev, controles = decidir(s, cfg)
        out = {
            "id_solicitud": s["id_solicitud"],
            "herramienta_simulada": s["herramienta_simulada"],
            "accion_solicitada": s["accion_solicitada"],
            "decision_defensiva": decision,
            "motivo_decision": motivo,
            "controles_aplicados": controles,
            "requiere_revision_humana": rev,
            "registro_generado": str((reg_dir / f"{s['id_solicitud']}.json").as_posix()),
            "recomendacion": "Mantener trazabilidad y revisión de casos sensibles.",
            "usa_herramienta_real": False,
            "ejecuta_comando_real": False,
            "usa_ia_real": False,
            "usa_api_externa": False,
            "usa_cloud": False,
        }
        (reg_dir / f"{s['id_solicitud']}.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
        resultados.append(out)

    return {
        "fecha_generacion": datetime.now().isoformat(timespec="seconds"),
        "total_solicitudes_analizadas": len(resultados),
        "errores_validacion": errores,
        "resumen_por_herramienta": dict(Counter(r["herramienta_simulada"] for r in resultados)),
        "resumen_por_decision": dict(Counter(r["decision_defensiva"] for r in resultados)),
        "acciones_bloqueadas": [r["accion_solicitada"] for r in resultados if r["decision_defensiva"] == "bloquear"],
        "controles_defensivos_aplicados": cfg["controles_defensivos"],
        "resultados": resultados,
    }


def generar_md(r: dict[str, Any]) -> str:
    dec = r["resumen_por_decision"]
    lines = [
        "# Informe de Control Defensivo de Herramientas Simuladas",
        "",
        f"Fecha de generación: {r['fecha_generacion']}",
        "",
        "## Resumen ejecutivo",
        "Control local de uso simulado de herramientas con decisiones defensivas de permitir, bloquear o revisar.",
        "",
        "## Total de solicitudes analizadas",
        str(r["total_solicitudes_analizadas"]),
        "",
        f"## Decisiones permitidas\n{dec.get('permitir', 0)}",
        "",
        f"## Decisiones bloqueadas\n{dec.get('bloquear', 0)}",
        "",
        f"## Decisiones con revisión humana\n{dec.get('revisar', 0)}",
        "",
        "## Herramientas más solicitadas",
    ]
    lines.extend([f"- {k}: {v}" for k, v in r["resumen_por_herramienta"].items()])
    lines += ["", "## Acciones bloqueadas"]
    lines.extend([f"- {a}" for a in r["acciones_bloqueadas"]] or ["- Ninguna"])
    lines += ["", "## Controles defensivos aplicados"]
    lines.extend([f"- {c}" for c in r["controles_defensivos_aplicados"]])
    lines += [
        "",
        "## Lectura técnica defensiva",
        "Las solicitudes restringidas o de alta sensibilidad se bloquean o escalan a revisión humana.",
        "",
        "## Límites del control",
        "No ejecuta herramientas reales ni comandos del sistema; solo escenarios sintéticos.",
        "",
        "## Recomendaciones siguientes",
        "1. Ajustar catálogo de herramientas por dominio.",
        "2. Reforzar revisión en sensibilidad alta.",
        "3. Auditar registros periódicamente.",
        "",
        "## 🪪 Licencia y Autoría",
        "Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  ",
        "© 2025 – Txema Ríos. Todos los derechos compartidos.",
    ]
    return "\n".join(lines) + "\n"


def ejecutar(rq: Path, cfg: Path, out_md: Path, out_json: Path, reg_dir: Path) -> dict[str, Any]:
    solicitudes = cargar_json(rq)
    config = cargar_json(cfg)
    resultado = procesar(solicitudes, config, reg_dir)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(generar_md(resultado), encoding="utf-8")
    out_json.write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8")
    return resultado


def main() -> None:
    p = argparse.ArgumentParser(description="Control local defensivo de herramientas simuladas.")
    p.add_argument("--requests", required=True, type=Path)
    p.add_argument("--config", required=True, type=Path)
    p.add_argument("--output-md", required=True, type=Path)
    p.add_argument("--output-json", required=True, type=Path)
    p.add_argument("--registry-dir", required=True, type=Path)
    a = p.parse_args()
    r = ejecutar(a.requests, a.config, a.output_md, a.output_json, a.registry_dir)
    print(f"Control completado. Solicitudes válidas: {r['total_solicitudes_analizadas']}")


if __name__ == "__main__":
    main()
