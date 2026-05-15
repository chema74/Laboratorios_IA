import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from app.config import RUTA_INFORME_MULTI
from evaluacion.evaluador_resultados import evaluar_resultado
from evaluacion.evaluador_trazabilidad import evaluar_trazabilidad
from observabilidad.costes_simulados import coste_ejecucion
from orquestacion.motor_orquestacion import ejecutar_escenario


def main() -> None:
    r = ejecutar_escenario("ESC-002")
    ev = evaluar_resultado(r)
    traz = evaluar_trazabilidad(r)
    coste = coste_ejecucion(r)

    lineas = [
        "# Escenario Multiagente",
        "- Escenario: ESC-002",
        f"- Tarea: {r.get('id_tarea')}",
        f"- Estado final: {r['estado_final']}",
        f"- Resultados parciales: {len(r['ejecucion']['resultados'])}",
        f"- Riesgos revisión: {r['revision']['riesgos']}",
        f"- Trazabilidad suficiente: {traz['suficiente']}",
        f"- Score resultado: {ev['score']}",
        f"- Coste simulado: {coste['coste_total_simulado_eur']} EUR",
    ]
    RUTA_INFORME_MULTI.parent.mkdir(parents=True, exist_ok=True)
    RUTA_INFORME_MULTI.write_text("\n".join(lineas), encoding="utf-8")
    print(f"Informe multiagente: {RUTA_INFORME_MULTI}")


if __name__ == "__main__":
    main()
