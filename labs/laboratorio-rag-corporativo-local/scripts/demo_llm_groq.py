import json
import sys
from datetime import UTC, datetime
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from app.config import RUTA_EVIDENCIAS, RUTA_INFORME_DEMO_LLM, RUTA_RESULTADO_DEMO_LLM
from servicios.analisis_llm import analizar_rag_llm
from servicios.rag_llm import ejecutar_rag_con_llm

CONSULTA_DEMO = "¿Qué riesgos aparecen en los documentos de cumplimiento?"


def _texto_seguro(valor: object) -> str:
    if isinstance(valor, str):
        return valor
    try:
        return json.dumps(valor, ensure_ascii=False)
    except Exception:
        return str(valor)


def _render_markdown(resultado: dict) -> str:
    llm = resultado["analisis_llm"]
    resp = llm["respuesta"]
    riesgos = resp.get("riesgos", [])
    recomendaciones = resp.get("recomendaciones", [])
    trazas = llm.get("trazabilidad", {})

    lineas = [
        "# Demo RAG + LLM Groq V2.1",
        "",
        f"- Fecha UTC: {resultado['metadata']['fecha_utc']}",
        f"- Consulta: {resultado['consulta']}",
        f"- Proveedor: {llm.get('proveedor', 'desconocido')}",
        f"- Modelo: {llm.get('modelo', trazas.get('groq_model', 'n/a'))}",
        f"- Ruta de ejecución: {trazas.get('ruta_ejecucion', 'indefinida')}",
    ]
    if llm.get("motivo_fallback"):
        lineas.append(f"- Motivo fallback: {llm['motivo_fallback']}")

    lineas.extend(["", "## Fragmentos recuperados"])
    for f in resultado.get("rag", {}).get("fragmentos", [])[:3]:
        lineas.append(f"- {f.get('doc_id')} / {f.get('titulo')}: {str(f.get('contenido', ''))[:180]}...")

    lineas.extend(["", "## Resumen ejecutivo", _texto_seguro(resp.get("resumen", "Sin resumen")), "", "## Riesgos"])
    for r in riesgos:
        lineas.append(f"- {r}")

    lineas.extend(["", "## Recomendaciones"])
    for rec in recomendaciones:
        lineas.append(f"- {rec}")

    lineas.extend([
        "",
        "## Licencia y Autoría",
        "Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.",
        "",
        "© 2026 – Txema Ríos.",
    ])
    return "\n".join(lineas)


def main() -> None:
    RUTA_EVIDENCIAS.mkdir(parents=True, exist_ok=True)
    rag = ejecutar_rag_con_llm(CONSULTA_DEMO)
    llm = analizar_rag_llm(CONSULTA_DEMO, rag["fragmentos"])
    resultado = {
        "metadata": {"version": "V2.1", "fecha_utc": datetime.now(UTC).isoformat()},
        "consulta": CONSULTA_DEMO,
        "rag": rag,
        "analisis_llm": llm,
    }

    RUTA_RESULTADO_DEMO_LLM.write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8")
    RUTA_INFORME_DEMO_LLM.write_text(_render_markdown(resultado), encoding="utf-8")

    print("Demo RAG LLM V2.1 completada")
    print(f"- Resultado JSON: {RUTA_RESULTADO_DEMO_LLM}")
    print(f"- Informe Markdown: {RUTA_INFORME_DEMO_LLM}")
    print(f"- Proveedor utilizado: {llm.get('proveedor')}")
    print(f"- Ruta de ejecución: {llm.get('trazabilidad', {}).get('ruta_ejecucion', 'n/a')}")
    print(f"- Modelo: {llm.get('modelo', llm.get('trazabilidad', {}).get('groq_model', 'n/a'))}")
    if llm.get("motivo_fallback"):
        print(f"- Motivo fallback: {llm['motivo_fallback']}")


if __name__ == "__main__":
    main()
