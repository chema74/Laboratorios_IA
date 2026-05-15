import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from app.config import RUTA_RESULTADOS
from servicios.pipeline_rag import ejecutar_pipeline

CONSULTAS_DEMO = [
    "¿Cuál es el SLA para incidencias críticas de soporte?",
    "Requisitos de contraseñas corporativas en seguridad",
    "Cómo se aprueban compras TIC de más de 2000 euros",
]


def main() -> None:
    RUTA_RESULTADOS.mkdir(parents=True, exist_ok=True)
    lineas = ["# Demo RAG Corporativo Local V1", ""]

    for i, q in enumerate(CONSULTAS_DEMO, start=1):
        res = ejecutar_pipeline(q)
        print(f"\n[{i}] Consulta: {q}")
        print(f"Respuesta: {res['respuesta']}")
        print(f"Citas: {', '.join(res['citas']) if res['citas'] else 'sin citas'}")
        top_score = res["resultados"][0]["puntuacion"] if res["resultados"] else 0.0
        print(f"Top score: {top_score}")
        print(f"Trazas: {len(res['trazas'])} eventos")

        lineas.extend([
            f"## Consulta {i}",
            f"- Consulta: {q}",
            f"- Respuesta: {res['respuesta']}",
            f"- Citas: {', '.join(res['citas']) if res['citas'] else 'sin citas'}",
            f"- Top score: {top_score}",
            f"- Eventos traza: {len(res['trazas'])}",
            "",
        ])

    destino = RUTA_RESULTADOS / "demo_rag_corporativo.md"
    destino.write_text("\n".join(lineas), encoding="utf-8")
    print(f"\nInforme demo generado en: {destino}")


if __name__ == "__main__":
    main()
