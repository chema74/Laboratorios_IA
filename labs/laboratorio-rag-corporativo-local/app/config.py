from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
RUTA_DATOS_BRUTOS = RAIZ / "datos" / "brutos" / "documentos_corporativos.json"
RUTA_DATASET_DORADO = RAIZ / "evaluacion" / "dataset_dorado.json"
RUTA_RESULTADOS = RAIZ / "evaluacion" / "resultados"
RUTA_EVIDENCIAS = RAIZ / "evidencias"
RUTA_EVIDENCIAS_INTERACTIVAS = RUTA_EVIDENCIAS / "interactivas"
RUTA_RESULTADO_DEMO_LLM = RUTA_EVIDENCIAS / "resultado_demo_llm_groq.json"
RUTA_INFORME_DEMO_LLM = RUTA_EVIDENCIAS / "demo_llm_groq.md"
RUTA_PANEL_DEMO = RUTA_EVIDENCIAS / "panel_demo.html"
MAX_CARACTERES_CONSULTA = 280
TOP_K_RECUPERACION = 5
