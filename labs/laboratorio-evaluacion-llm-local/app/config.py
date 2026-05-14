from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
RUTA_DATASET = RAIZ / "datos" / "dataset_dorado.json"
RUTA_RESPUESTAS = RAIZ / "datos" / "respuestas_sinteticas.json"
RUTA_PROMPTS = RAIZ / "datos" / "prompts_versionados.json"
RUTA_RESULTADOS = RAIZ / "evaluacion" / "resultados"
