from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
RUTA_CASOS = RAIZ / "datos" / "casos_uso_ia.json"
RUTA_MATRIZ = RAIZ / "datos" / "matriz_riesgos.json"
RUTA_OBLIG = RAIZ / "datos" / "obligaciones_orientativas.json"
RUTA_EVID = RAIZ / "datos" / "evidencias_gobernanza.json"
RUTA_SHADOW = RAIZ / "datos" / "shadow_ia_sintetica.json"
RUTA_INFORME = RAIZ / "informes" / "informe_gobernanza_ai_act.md"
RUTA_FICHAS = RAIZ / "informes" / "fichas_sistemas_ia"
