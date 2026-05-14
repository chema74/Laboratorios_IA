import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from app.config import RUTA_FICHAS, RUTA_INFORME
from servicios.generador_informes import generar_informe
from servicios.motor_gobernanza import ejecutar_motor


def main() -> None:
    r = ejecutar_motor()
    ruta, fichas = generar_informe(r, RUTA_INFORME, RUTA_FICHAS)
    print("Demo gobernanza AI Act local")
    print(f"- Casos inventariados: {r['resumen_inventario']['total']}")
    print(f"- Shadow IA detectado: {len(r['shadow_ia'])}")
    print(f"- Evidencias faltantes: {len(r['evidencias_faltantes'])}")
    print(f"- Informe: {ruta}")
    print(f"- Fichas generadas: {len(fichas)}")


if __name__ == "__main__":
    main()
