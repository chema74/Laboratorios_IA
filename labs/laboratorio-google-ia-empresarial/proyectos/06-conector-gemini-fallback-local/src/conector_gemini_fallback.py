"""Conector conceptual Gemini con fallback local obligatorio (V1)."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime
from pathlib import Path


def cargar_json(ruta: Path) -> dict:
    with ruta.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def validar_solicitudes(solicitudes: list[dict], config: dict) -> None:
    tipos = set(config["tipos_solicitud_permitidos"])
    for s in solicitudes:
        if s["tipo_solicitud"] not in tipos:
            raise ValueError(f"Tipo no permitido: {s['tipo_solicitud']}")
        if s["requiere_gemini_real"] or s["usa_gemini_real"] or s["usa_api_externa"] or s["usa_cloud"] or s["usa_ia_real"]:
            raise ValueError(f"Solicitud inválida por dependencia real: {s['id_solicitud']}")
        if not s["fallback_obligatorio"]:
            raise ValueError(f"Fallback obligatorio ausente: {s['id_solicitud']}")


def verificar_modo(config: dict) -> None:
    if config["modo_v1"] != "fallback-local":
        raise ValueError("Modo V1 inválido.")
    if config["permitir_api_real"]:
        raise ValueError("API real no permitida en V1.")


def respuesta_determinista(s: dict, config: dict) -> str:
    plantilla = config["reglas_respuesta_fallback"]["plantilla"]
    return plantilla.format(tipo=s["tipo_solicitud"], contexto=s["contexto_sintetico"])


def guardar_registro(dir_resp: Path, resultado: dict) -> str:
    dir_resp.mkdir(parents=True, exist_ok=True)
    ruta = dir_resp / f"{resultado['id_solicitud']}.json"
    ruta.write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(ruta)


def procesar(data: dict, config: dict, dir_resp: Path) -> list[dict]:
    verificar_modo(config)
    solicitudes = data["solicitudes"]
    validar_solicitudes(solicitudes, config)
    out = []
    for s in solicitudes:
        r = {
            "id_solicitud": s["id_solicitud"],
            "tipo_solicitud": s["tipo_solicitud"],
            "modo_ejecucion": "fallback-local",
            "respuesta_simulada": respuesta_determinista(s, config),
            "razon_fallback": s["razon_fallback"],
            "trazabilidad_fallback": f"fallback_local::{s['id_solicitud']}::{s['razon_fallback']}",
            "registro_generado": "",
            "usa_gemini_real": False,
            "usa_api_externa": False,
            "usa_cloud": False,
            "usa_ia_real": False,
        }
        r["registro_generado"] = guardar_registro(dir_resp, r)
        out.append(r)
    return out


def resumen_global(resultados: list[dict], config: dict) -> dict:
    return {
        "fecha_generacion": datetime.now().isoformat(timespec="seconds"),
        "total_solicitudes": len(resultados),
        "solicitudes_por_tipo": dict(Counter(x["tipo_solicitud"] for x in resultados)),
        "motivos_fallback": dict(Counter(x["razon_fallback"] for x in resultados)),
        "trazabilidad_fallback": [x["trazabilidad_fallback"] for x in resultados],
        "respuestas_simuladas_generadas": [x["respuesta_simulada"] for x in resultados],
        "modo_v1": config["modo_v1"],
        "nota": config["nota"],
        "resultados": resultados,
    }


def generar_md(resultado: dict, output_md: Path) -> None:
    l = [
        "# Informe de Gemini Fallback Local (V1)",
        "",
        f"**Fecha de generación:** {resultado['fecha_generacion']}",
        "",
        "## Resumen ejecutivo",
        "Todas las solicitudes se procesaron por fallback local sin Gemini API real, sin red y sin IA real.",
        "",
        "## Total de solicitudes",
        f"- {resultado['total_solicitudes']}",
        "",
        "## Solicitudes por tipo",
    ]
    for k, v in resultado["solicitudes_por_tipo"].items():
        l.append(f"- {k}: {v}")
    l.extend(["", "## Motivos de fallback"])
    for k, v in resultado["motivos_fallback"].items():
        l.append(f"- {k}: {v}")
    l.extend(["", "## Respuestas simuladas generadas"])
    for x in resultado["respuestas_simuladas_generadas"][:6]:
        l.append(f"- {x}")
    l.extend(["", "## Trazabilidad de fallback"])
    for t in resultado["trazabilidad_fallback"][:8]:
        l.append(f"- {t}")
    l.extend(
        [
            "",
            "## Límites de la V1",
            "Sin Gemini API real, sin claves reales, sin Google Cloud, sin red y sin IA real.",
            "",
            "## Posible V2 futura con .env y fallback local",
            "V2 podrá documentar variables `.env` para API opcional, manteniendo fallback local por defecto.",
            "",
            "## Recomendaciones siguientes",
            "1. Añadir más tipos de solicitud sintética.",
            "2. Conectar trazabilidad con el módulo 08.",
            "3. Mantener política de bloqueo de red en pruebas locales.",
            "",
            "## 🪪 Licencia y Autoría",
            "Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  ",
            "© 2025 – Txema Ríos. Todos los derechos compartidos.",
        ]
    )
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text("\n".join(l), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Conector Gemini fallback local")
    p.add_argument("--requests", required=True)
    p.add_argument("--config", required=True)
    p.add_argument("--output-md", required=True)
    p.add_argument("--output-json", required=True)
    p.add_argument("--responses-dir", required=True)
    return p.parse_args()


def main() -> None:
    a = parse_args()
    data = cargar_json(Path(a.requests))
    config = cargar_json(Path(a.config))
    resultados = procesar(data, config, Path(a.responses_dir))
    out = resumen_global(resultados, config)
    out_json = Path(a.output_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    generar_md(out, Path(a.output_md))


if __name__ == "__main__":
    main()
