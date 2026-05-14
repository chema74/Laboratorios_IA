import json
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from app.config import RUTA_EVIDENCIAS, RUTA_INFORME_DEMO_LLM, RUTA_RESULTADO_DEMO_LLM
from servicios.analisis_llm import analizar_privacidad_llm
from servicios.motor_privacidad import ejecutar_motor


def _render_markdown(resultado: dict) -> str:
    llm = resultado["analisis_llm"]
    resp = llm["respuesta"]
    riesgos = resp.get("riesgos", [])
    recomendaciones = resp.get("recomendaciones", [])
    trazas = llm.get("trazabilidad", {})
    lineas = [
        "# Demo LLM Groq V2.1",
        "",
        f"- Fecha UTC: {resultado['metadata']['fecha_utc']}",
        f"- Proveedor: {llm.get('proveedor', 'desconocido')}",
        f"- Modo: {llm.get('modo', 'desconocido')}",
        f"- Modelo: {llm.get('modelo', trazas.get('groq_model', 'n/a'))}",
    ]
    if "motivo_fallback" in llm:
        lineas.append(f"- Motivo fallback: {llm['motivo_fallback']}")
    lineas.extend([
        "",
        "## Resumen",
        resp.get("resumen", "Sin resumen."),
        "",
        "## Riesgos",
    ])
    for r in riesgos:
        lineas.append(f"- {r}")
    lineas.extend(["", "## Recomendaciones"])
    for rec in recomendaciones:
        lineas.append(f"- {rec}")

    lineas.extend(["", "## Trazabilidad LLM"])
    for k, v in trazas.items():
        lineas.append(f"- {k}: {v}")

    lineas.extend([
        "",
        "## Trazabilidad",
        f"- Casos analizados: {len(resultado['motor_privacidad'].get('analisis_casos', []))}",
        f"- Riesgo motor base: {resultado['motor_privacidad'].get('evaluacion_exposicion', {}).get('nivel_riesgo', 'desconocido')}",
        "",
        "## Licencia y Autoría",
        "Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.",
        "",
        "© 2026 – Txema Ríos.",
    ])
    return "\n".join(lineas)


def main() -> None:
    RUTA_EVIDENCIAS.mkdir(parents=True, exist_ok=True)
    base = ejecutar_motor()
    analisis_llm = analizar_privacidad_llm(base)
    resultado = {
        "metadata": {"version": "V2.1", "fecha_utc": datetime.now(timezone.utc).isoformat()},
        "motor_privacidad": base,
        "analisis_llm": analisis_llm,
    }
    RUTA_RESULTADO_DEMO_LLM.write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8")
    RUTA_INFORME_DEMO_LLM.write_text(_render_markdown(resultado), encoding="utf-8")

    print("Demo LLM V2.1 completada")
    print(f"- Resultado JSON: {RUTA_RESULTADO_DEMO_LLM}")
    print(f"- Informe Markdown: {RUTA_INFORME_DEMO_LLM}")
    print(f"- Proveedor utilizado: {analisis_llm.get('proveedor')}")
    print(f"- Ruta de ejecución: {analisis_llm.get('trazabilidad', {}).get('ruta_ejecucion', 'n/a')}")
    print(f"- Modelo: {analisis_llm.get('modelo', analisis_llm.get('trazabilidad', {}).get('groq_model', 'n/a'))}")
    if analisis_llm.get("motivo_fallback"):
        print(f"- Motivo fallback: {analisis_llm['motivo_fallback']}")


if __name__ == "__main__":
    main()
