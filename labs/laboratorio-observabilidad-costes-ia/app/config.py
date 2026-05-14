from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
RUTA_EVENTOS = RAIZ / "datos" / "eventos_ia_sinteticos.json"
RUTA_PRESUPUESTO = RAIZ / "datos" / "presupuesto_operativo.json"
RUTA_FEEDBACK = RAIZ / "datos" / "feedback_usuarios.json"
RUTA_INFORME = RAIZ / "informes" / "informe_observabilidad_costes_ia.md"
RUTA_PANEL = RAIZ / "panel" / "panel_observabilidad.html"
