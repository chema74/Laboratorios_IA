import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from servicios.evaluacion_llm_v21 import cargar_casos_demo, evaluar_respuesta_llm, guardar_evidencia_json


def _licencia_md() -> str:
    return (
        "\n---\n\n"
        "## Licencia y Autoría\n"
        "Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.\n"
        "© 2026 - Txema Ríos.\n"
    )


def _render_markdown(resultados: list[dict], casos_por_id: dict[str, dict]) -> str:
    lineas = [
        "# Demo LLM Groq Opcional V2.1",
        "",
        "Evidencia de evaluación con ruta Groq opcional y fallback local determinista.",
        "",
    ]
    for r in resultados:
        caso = casos_por_id.get(r["escenario"], {})
        nombre = caso.get("nombre", r["escenario"])
        descripcion = caso.get("descripcion", "")
        lineas.extend([
            f"## Caso: {nombre}",
            "",
            f"- Id escenario: `{r['escenario']}`",
            f"- Descripción: {descripcion}",
            f"- Proveedor: `{r['proveedor']}`",
            f"- Modelo: `{r['modelo']}`",
            f"- Ruta ejecución: `{r['ruta_ejecucion']}`",
            f"- Motivo fallback: `{r['motivo_fallback']}`",
            f"- Puntuación media: `{r['puntuacion_media']}`",
            f"- Riesgos: `{', '.join(r['riesgos']) if r['riesgos'] else 'ninguno'}`",
            "",
        ])
    lineas.append(_licencia_md())
    return "\n".join(lineas)


def _valor_caso(caso: dict, principal: str, *aliases: str, default: str = "") -> str:
    for key in (principal, *aliases):
        value = caso.get(key)
        if isinstance(value, str) and value.strip():
            return value
    return default


def main() -> None:
    casos = cargar_casos_demo(BASE / "datos" / "casos_demo_llm_v21.json")
    resultados = []

    for caso in casos:
        escenario = _valor_caso(caso, "id", default="escenario_sin_id")
        pregunta = _valor_caso(caso, "pregunta", default="")
        contexto = _valor_caso(caso, "contexto_esperado", "contexto", default="")
        respuesta = _valor_caso(caso, "respuesta_candidata", "respuesta", default="")
        criterios = caso.get("criterios") if isinstance(caso.get("criterios"), list) and caso.get("criterios") else [
            "relevancia", "precision", "cobertura", "seguridad", "consistencia", "trazabilidad"
        ]

        res = evaluar_respuesta_llm(
            escenario=escenario,
            pregunta=pregunta,
            contexto=contexto,
            respuesta_candidata=respuesta,
            criterios=criterios,
        )
        resultados.append(res)

    salida_json = {
        "fecha_utc": resultados[0]["fecha_utc"] if resultados else "",
        "total_casos": len(resultados),
        "resultados": resultados,
    }

    ruta_json = guardar_evidencia_json(salida_json, BASE / "evidencias" / "resultado_demo_llm_groq.json")
    ruta_md = BASE / "evidencias" / "demo_llm_groq.md"
    ruta_md.parent.mkdir(parents=True, exist_ok=True)
    casos_por_id = {c.get("id", f"idx_{i}"): c for i, c in enumerate(casos)}
    ruta_md.write_text(_render_markdown(resultados, casos_por_id), encoding="utf-8")

    print("Demo LLM V2.1 completada")
    print(f"Casos evaluados: {len(resultados)}")
    print(f"Evidencia JSON: {ruta_json}")
    print(f"Evidencia Markdown: {ruta_md}")
    if resultados:
        print(f"Último proveedor: {resultados[-1]['proveedor']}")
        print(f"Última ruta: {resultados[-1]['ruta_ejecucion']}")
        print(f"Último motivo_fallback: {resultados[-1]['motivo_fallback']}")


if __name__ == "__main__":
    main()
