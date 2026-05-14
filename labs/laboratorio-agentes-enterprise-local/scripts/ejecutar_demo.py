import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from app.config import RUTA_INFORME_DEMO
from evaluacion.evaluador_resultados import evaluar_resultado
from evaluacion.evaluador_trazabilidad import evaluar_trazabilidad
from observabilidad.costes_simulados import coste_ejecucion
from orquestacion.motor_orquestacion import ejecutar_escenario


def main() -> None:
    r = ejecutar_escenario("ESC-001")
    ev = evaluar_resultado(r)
    traz = evaluar_trazabilidad(r)
    coste = coste_ejecucion(r)

    print("Demo agentes enterprise")
    print(f"- Tarea: {r.get('id_tarea')}")
    print(f"- Pasos plan: {len(r['plan']['pasos'])}")
    print(f"- Herramientas: {', '.join(r['plan']['herramientas'])}")
    print(f"- Bloqueos: {len(r['ejecucion']['bloqueos'])}")
    print(f"- Estado final: {r['estado_final']}")
    print(f"- Score evaluación: {ev['score']}")

    lineas = [
        "# Demo Agentes Enterprise",
        f"- Tarea: {r.get('id_tarea')}",
        f"- Estado final: {r['estado_final']}",
        f"- Pasos ejecutados: {len(r['ejecucion']['resultados'])}",
        f"- Bloqueos: {len(r['ejecucion']['bloqueos'])}",
        f"- Score resultado: {ev['score']}",
        f"- Trazabilidad suficiente: {traz['suficiente']}",
        f"- Coste simulado: {coste['coste_total_simulado_eur']} EUR",
    ]
    RUTA_INFORME_DEMO.parent.mkdir(parents=True, exist_ok=True)
    RUTA_INFORME_DEMO.write_text("\n".join(lineas), encoding="utf-8")
    print(f"Informe demo: {RUTA_INFORME_DEMO}")


if __name__ == "__main__":
    main()
