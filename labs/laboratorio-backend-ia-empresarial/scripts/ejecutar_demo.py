import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from app.config import RUTA_INFORME, RUTA_PETICIONES, RUTA_TAREAS, RUTA_USUARIOS
from colas.cola_simulada import ColaSimulada
from colas.procesador_tareas import procesar_pendientes
from observabilidad.metricas import calcular_metricas
from servicios.generador_informes import generar_informe
from servicios.motor_backend import ejecutar_lote


def main() -> None:
    lote = ejecutar_lote(RUTA_PETICIONES, RUTA_USUARIOS)

    with RUTA_TAREAS.open("r", encoding="utf-8-sig") as f:
        tareas = json.load(f)
    cola = ColaSimulada(tareas)
    proc = procesar_pendientes(cola)

    metricas = calcular_metricas(lote["bitacora"], len(proc["completadas"]))
    resumen = {"metricas": metricas, "coste": lote["coste"]}
    ruta = generar_informe(RUTA_INFORME, resumen)

    print("Demo backend IA empresarial")
    print(f"- Peticiones: {metricas['total_peticiones']}")
    print(f"- Éxitos: {metricas['exito']} | Errores: {metricas['error']}")
    print(f"- Tareas completadas: {len(proc['completadas'])}")
    print(f"- Informe: {ruta}")


if __name__ == "__main__":
    main()
