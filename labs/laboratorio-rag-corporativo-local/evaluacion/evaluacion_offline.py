import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from app.config import RUTA_DATASET_DORADO, RUTA_RESULTADOS
from servicios.pipeline_rag import ejecutar_pipeline


def evaluar() -> dict:
    with RUTA_DATASET_DORADO.open("r", encoding="utf-8-sig") as f:
        casos = json.load(f)

    aciertos = 0
    resultados = []
    for caso in casos:
        salida = ejecutar_pipeline(caso["consulta"])
        recuperados = {c[0:7] for c in salida["citas"]}
        esperados = set(caso["documentos_esperados"])
        hit = bool(recuperados & esperados)
        aciertos += 1 if hit else 0
        resultados.append({
            "id": caso["id"],
            "consulta": caso["consulta"],
            "hit": hit,
            "esperados": sorted(esperados),
            "recuperados": sorted(recuperados),
        })

    precision = aciertos / max(len(casos), 1)
    return {"total": len(casos), "aciertos": aciertos, "precision": precision, "resultados": resultados}


def generar_informe(metricas: dict) -> Path:
    RUTA_RESULTADOS.mkdir(parents=True, exist_ok=True)
    destino = RUTA_RESULTADOS / "resultado_evaluacion.md"
    lineas = [
        "# Evaluación Offline RAG V1",
        "",
        f"- Total consultas: {metricas['total']}",
        f"- Aciertos: {metricas['aciertos']}",
        f"- Precisión@1 aproximada: {metricas['precision']:.2f}",
        "",
        "## Detalle",
        "",
    ]
    for r in metricas["resultados"]:
        lineas.append(f"- {r['id']}: {'OK' if r['hit'] else 'FAIL'} | esperados={r['esperados']} | recuperados={r['recuperados']}")
    destino.write_text("\n".join(lineas), encoding="utf-8")
    return destino


def main() -> None:
    metricas = evaluar()
    ruta = generar_informe(metricas)
    print(f"Evaluación completada. Informe: {ruta}")


if __name__ == "__main__":
    main()
