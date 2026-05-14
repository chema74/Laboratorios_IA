import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from app.config import RUTA_INFORME
from scripts.generar_panel import main as generar_panel
from servicios.generador_informes import generar_informe
from servicios.motor_observabilidad import ejecutar_motor_observabilidad


def main() -> None:
    resultado = ejecutar_motor_observabilidad()
    informe = generar_informe(resultado, RUTA_INFORME)
    print("Resumen demo observabilidad:")
    print(f"- Eventos: {resultado['resumen_eventos']['total']}")
    print(f"- Coste total: {resultado['costes']['coste_total']} EUR")
    print(f"- P95 latencia: {resultado['latencias']['p95_aprox']} ms")
    print(f"- Alertas: {len(resultado['alertas_degradacion'])}")
    print(f"Informe: {informe}")
    generar_panel()


if __name__ == "__main__":
    main()
