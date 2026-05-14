from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
RUTA_DATASET = RAIZ / "datos" / "dataset_con_pii_sintetica.json"
RUTA_POLITICAS = RAIZ / "datos" / "politicas_privacidad_sinteticas.json"
RUTA_PROMPTS = RAIZ / "datos" / "prompts_con_contexto_sensible.json"
RUTA_SALIDAS = RAIZ / "datos" / "salidas_ia_sinteticas.json"
RUTA_REGISTRO = RAIZ / "datos" / "registro_tratamiento_sintetico.json"
RUTA_INFORME = RAIZ / "informes" / "informe_privacidad_datos_ia.md"
RUTA_EVIDENCIAS = RAIZ / "evidencias"
RUTA_RESULTADO_DEMO_LLM = RUTA_EVIDENCIAS / "resultado_demo_llm_groq.json"
RUTA_INFORME_DEMO_LLM = RUTA_EVIDENCIAS / "demo_llm_groq.md"
RUTA_PANEL_DEMO = RUTA_EVIDENCIAS / "panel_demo.html"
