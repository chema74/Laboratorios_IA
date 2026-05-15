from __future__ import annotations

import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
SRC = BASE / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from observabilidad_costes_ia.escenarios import obtener_escenario
from observabilidad_costes_ia.motor import analizar_eventos
from observabilidad_costes_ia.orquestador import generar_analisis_ejecutivo

LICENCIA = """\nPublicado bajo licencia Creative Commons CC BY-SA 4.0 International.
© 2025 - Txema Rios. Todos los derechos compartidos.
"""


def _salida_dir() -> Path:
    custom = os.getenv("ARTIFACTS_DIR", "").strip()
    if custom:
        return Path(custom) / "evidencias" / "v2_1"
    return BASE / "evidencias" / "v2_1"


def _normalizar_texto(valor: object) -> str:
    if isinstance(valor, str):
        return valor
    if valor is None:
        return ""
    return json.dumps(valor, ensure_ascii=False)


def generar_evidencias(escenario: str = "uso_normal_controlado") -> dict[str, Path]:
    eventos = obtener_escenario(escenario)
    metrica = analizar_eventos(eventos)
    analisis = generar_analisis_ejecutivo(metrica)
    marca_tiempo = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")

    diagnostico = analisis.get("diagnostico_groq") or {
        "solicitado": False,
        "estado": "no_solicitado",
        "categoria": "sin_diagnostico",
        "http_status": None,
        "modelo_usado": None,
        "mensaje_seguro": "No se recibio diagnostico Groq; se asume fallback local.",
    }

    resumen_ejecutivo = _normalizar_texto(analisis.get("resumen_ejecutivo", ""))
    paquete = {
        "escenario": escenario,
        "modo": analisis.get("modo", "fallback_local"),
        "timestamp_generacion": marca_tiempo,
        "resumen_ejecutivo": resumen_ejecutivo,
        "metricas_agregadas": {k: v for k, v in metrica.items() if k != "eventos"},
        "eventos_analizados": metrica["eventos"],
        "alertas": metrica["alertas"],
        "recomendaciones": {
            "coste": analisis.get("recomendaciones_optimizacion_coste", []),
            "operacion": analisis.get("recomendaciones_operacion", []),
            "gobernanza": analisis.get("alertas_gobernanza_uso_responsable", []),
        },
        "diagnostico_groq": diagnostico,
    }

    salida = _salida_dir()
    salida.mkdir(parents=True, exist_ok=True)
    ruta_json = salida / "evidencia_observabilidad_costes_v21.json"
    ruta_md = salida / "evidencia_observabilidad_costes_v21.md"
    ruta_html = salida / "evidencia_observabilidad_costes_v21.html"

    ruta_json.write_text(json.dumps(paquete, ensure_ascii=False, indent=2), encoding="utf-8")

    md = [
        "# Evidencia V2.1 - Observabilidad y Costes IA",
        "",
        f"- Escenario: `{escenario}`",
        f"- Modo: `{paquete['modo']}`",
        f"- Timestamp: `{marca_tiempo}`",
        "",
        "## Resumen ejecutivo",
        paquete["resumen_ejecutivo"],
        "",
        "## Diagnostico Groq / modo de ejecucion",
        "```json",
        json.dumps(paquete["diagnostico_groq"], ensure_ascii=False, indent=2),
        "```",
        "",
        "## Metricas agregadas",
        "```json",
        json.dumps(paquete["metricas_agregadas"], ensure_ascii=False, indent=2),
        "```",
        "",
        "## Alertas",
    ]
    md.extend([f"- {a['tipo']}: {a['detalle']}" for a in paquete["alertas"]] or ["- Sin alertas"])
    md.extend(["", "## Recomendaciones", "### Coste"])
    md.extend([f"- {item}" for item in paquete["recomendaciones"]["coste"]])
    md.append("### Operacion")
    md.extend([f"- {item}" for item in paquete["recomendaciones"]["operacion"]])
    md.append("### Gobernanza")
    md.extend([f"- {item}" for item in paquete["recomendaciones"]["gobernanza"]])
    md.append("")
    md.append(LICENCIA)
    ruta_md.write_text("\n".join(md), encoding="utf-8")

    filas = "".join(
        (
            f"<tr><td>{ev['id_evento']}</td><td>{ev['caso_uso']}</td><td>{ev['proveedor']}</td>"
            f"<td>{ev['modelo']}</td><td>{ev['latencia_ms']}</td><td>{ev['coste_estimado_eur']:.4f}</td>"
            f"<td>{ev['riesgo']}</td></tr>"
        )
        for ev in paquete["eventos_analizados"]
    )
    html = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Evidencia V2.1</title>
<style>body{{font-family:Segoe UI,Arial,sans-serif;margin:20px;background:#f8fafc}}.box{{background:#fff;border:1px solid #cbd5e1;padding:12px;border-radius:8px;margin-bottom:12px}}table{{width:100%;border-collapse:collapse}}td,th{{border:1px solid #cbd5e1;padding:6px}}</style></head>
<body><h1>Evidencia V2.1 - Observabilidad y Costes IA</h1>
<div class="box"><strong>Escenario:</strong> {escenario}<br><strong>Modo:</strong> {paquete['modo']}<br><strong>Timestamp:</strong> {marca_tiempo}</div>
<div class="box"><h2>Diagnostico Groq / modo de ejecucion</h2><pre>{json.dumps(paquete['diagnostico_groq'], ensure_ascii=False, indent=2)}</pre><p>Si Groq no esta disponible o falla, el laboratorio continua en fallback local de forma controlada.</p></div>
<div class="box"><h2>Resumen ejecutivo</h2><p>{paquete['resumen_ejecutivo']}</p></div>
<div class="box"><h2>Metricas agregadas</h2><pre>{json.dumps(paquete['metricas_agregadas'], ensure_ascii=False, indent=2)}</pre></div>
<div class="box"><h2>Eventos analizados</h2><table><thead><tr><th>ID</th><th>Caso</th><th>Proveedor</th><th>Modelo</th><th>Latencia</th><th>Coste</th><th>Riesgo</th></tr></thead><tbody>{filas}</tbody></table></div>
<p>Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.<br>© 2025 - Txema Rios. Todos los derechos compartidos.</p>
</body></html>"""
    ruta_html.write_text(html, encoding="utf-8")

    return {"json": ruta_json, "md": ruta_md, "html": ruta_html}


def main() -> int:
    rutas = generar_evidencias()
    print("Evidencias V2.1 generadas:")
    for tipo, ruta in rutas.items():
        print(f"- {tipo}: {ruta}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
