from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
RUTA_TAREAS = RAIZ / "datos" / "tareas_enterprise.json"
RUTA_HERRAMIENTAS = RAIZ / "datos" / "herramientas_simuladas.json"
RUTA_POLITICAS = RAIZ / "datos" / "politicas_agentes.json"
RUTA_ESCENARIOS = RAIZ / "datos" / "escenarios_multiagente.json"
RUTA_INFORME_DEMO = RAIZ / "informes" / "demo_agentes_enterprise.md"
RUTA_INFORME_MULTI = RAIZ / "informes" / "escenario_multiagente.md"
