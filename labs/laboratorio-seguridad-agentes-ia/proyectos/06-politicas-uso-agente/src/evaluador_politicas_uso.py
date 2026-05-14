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


def validar_caso(c: dict[str, Any]) -> list[str]:
    campos = [
        "id_caso", "agente_simulado", "descripcion_caso", "tipo_interaccion", "datos_implicados",
        "herramienta_solicitada", "accion_solicitada", "sensibilidad_simulada", "riesgo_operativo_simulado",
        "decision_esperada", "politica_esperada", "requiere_revision_humana", "limites_declarados",
        "usa_datos_reales", "usa_ia_real", "usa_api_externa", "usa_cloud", "nota_sintetica",
    ]
    return [f"Falta campo obligatorio: {x}" for x in campos if x not in c]


def activar_politica(caso: dict[str, Any], politicas: list[dict[str, Any]]) -> dict[str, Any]:
    # Prioriza política explícita de sensibilidad alta para forzar revisión humana defensiva.
    if caso.get("sensibilidad_simulada") == "alta":
        for p in politicas:
            if p["id_politica"] == "P-007":
                return p
    for p in politicas:
        if (
            p["aplica_a"] == caso["datos_implicados"]
            or p["aplica_a"] == caso["herramienta_solicitada"]
            or p["aplica_a"] == caso["sensibilidad_simulada"]
            or p["aplica_a"] == caso["tipo_interaccion"]
        ):
            return p
    return politicas[-1]


def evaluar(casos: list[dict[str, Any]], politicas: list[dict[str, Any]], reg_dir: Path) -> dict[str, Any]:
    reg_dir.mkdir(parents=True, exist_ok=True)
    errores: list[str] = []
    resultados: list[dict[str, Any]] = []
    for c in casos:
        err = validar_caso(c)
        for k in ("usa_datos_reales", "usa_ia_real", "usa_api_externa", "usa_cloud"):
            if c.get(k) is not False:
                err.append(f"{k} debe ser false")
        if err:
            errores.append(f"{c.get('id_caso','SIN_ID')}: " + " | ".join(err))
            continue
        pol = activar_politica(c, politicas)
        decision = pol["decision"]
        incumplimientos = []
        if decision != c["decision_esperada"]:
            incumplimientos.append("decision_no_coincide_esperada")
        if c["riesgo_operativo_simulado"] == "alto" and decision == "permitir":
            incumplimientos.append("permiso_en_riesgo_alto")
        if decision == "bloquear":
            incumplimientos.append("incumplimiento_politica_detectado")
        out = {
            "id_caso": c["id_caso"],
            "politica_activada": pol["id_politica"],
            "decision_defensiva": decision,
            "coincide_con_decision_esperada": decision == c["decision_esperada"],
            "controles_requeridos": pol["controles_requeridos"],
            "incumplimientos_detectados": incumplimientos,
            "requiere_revision_humana": decision == "revisar" or c["requiere_revision_humana"],
            "explicacion_defensiva": f"Se activa {pol['nombre_politica']} por reglas defensivas locales.",
            "registro_generado": str((reg_dir / f"{c['id_caso']}.json").as_posix()),
            "recomendacion": "Mantener trazabilidad y revisión de casos críticos.",
        }
        (reg_dir / f"{c['id_caso']}.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
        resultados.append(out)
    return {
        "fecha_generacion": datetime.now().isoformat(timespec="seconds"),
        "total_casos_evaluados": len(resultados),
        "errores_validacion": errores,
        "resumen_por_politica": dict(Counter(r["politica_activada"] for r in resultados)),
        "resumen_por_decision": dict(Counter(r["decision_defensiva"] for r in resultados)),
        "incumplimientos_simulados": [i for r in resultados for i in r["incumplimientos_detectados"]],
        "controles_requeridos": sorted({c for r in resultados for c in r["controles_requeridos"]}),
        "resultados": resultados,
    }


def generar_md(r: dict[str, Any]) -> str:
    dec = r["resumen_por_decision"]
    lines = [
        "# Informe de Evaluación de Políticas de Uso de Agente",
        "",
        f"Fecha de generación: {r['fecha_generacion']}",
        "",
        "## Resumen ejecutivo",
        "Evaluación local de casos sintéticos frente a políticas internas ficticias para decidir permitir, bloquear o revisar.",
        "",
        "## Total de casos evaluados",
        str(r["total_casos_evaluados"]),
        "",
        "## Políticas activadas",
    ]
    lines.extend([f"- {k}: {v}" for k, v in r["resumen_por_politica"].items()])
    lines += [
        "",
        f"## Decisiones permitidas\n{dec.get('permitir', 0)}",
        "",
        f"## Decisiones bloqueadas\n{dec.get('bloquear', 0)}",
        "",
        f"## Decisiones con revisión humana\n{dec.get('revisar', 0)}",
        "",
        "## Incumplimientos simulados",
    ]
    lines.extend([f"- {x}" for x in r["incumplimientos_simulados"]] or ["- Ninguno"])
    lines += ["", "## Controles requeridos"]
    lines.extend([f"- {c}" for c in r["controles_requeridos"]])
    lines += [
        "",
        "## Lectura técnica defensiva",
        "Las políticas restringen exposición sintética sensible y uso de herramientas de mayor riesgo.",
        "",
        "## Límites de la evaluación",
        "Análisis por reglas locales en casos ficticios; no aplica a producción.",
        "",
        "## Recomendaciones siguientes",
        "1. Ampliar cobertura de políticas por tipo de interacción.",
        "2. Revisar periódicamente casos con incumplimientos simulados.",
        "3. Vincular decisiones con matriz de riesgo global.",
        "",
        "## 🪪 Licencia y Autoría",
        "Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  ",
        "© 2025 – Txema Ríos. Todos los derechos compartidos.",
    ]
    return "\n".join(lines) + "\n"


def ejecutar(cases: Path, policies: Path, out_md: Path, out_json: Path, reg_dir: Path) -> dict[str, Any]:
    casos = cargar_json(cases)
    politicas = cargar_json(policies)
    r = evaluar(casos, politicas, reg_dir)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(generar_md(r), encoding="utf-8")
    out_json.write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")
    return r


def main() -> None:
    p = argparse.ArgumentParser(description="Evaluador local de políticas de uso de agente.")
    p.add_argument("--cases", required=True, type=Path)
    p.add_argument("--policies", required=True, type=Path)
    p.add_argument("--output-md", required=True, type=Path)
    p.add_argument("--output-json", required=True, type=Path)
    p.add_argument("--registry-dir", required=True, type=Path)
    a = p.parse_args()
    r = ejecutar(a.cases, a.policies, a.output_md, a.output_json, a.registry_dir)
    print(f"Evaluación completada. Casos válidos: {r['total_casos_evaluados']}")


if __name__ == "__main__":
    main()
