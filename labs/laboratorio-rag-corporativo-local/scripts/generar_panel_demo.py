import json
import sys
from html import escape
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from app.config import RUTA_PANEL_DEMO, RUTA_RESULTADO_DEMO_LLM


def _html(resultado: dict) -> str:
    llm = resultado.get("analisis_llm", {})
    resp = llm.get("respuesta", {})
    trazas = llm.get("trazabilidad", {})
    consulta = resultado.get("consulta", "")
    fragmentos = resultado.get("rag", {}).get("fragmentos", [])[:4]
    proveedor = llm.get("proveedor", "desconocido")
    modelo = llm.get("modelo", trazas.get("groq_model", "desconocido"))
    ruta = trazas.get("ruta_ejecucion", "indefinida")
    fallback = llm.get("motivo_fallback", "")

    riesgos = "".join(f"<li>{escape(str(x))}</li>" for x in resp.get("riesgos", [])) or "<li>Sin riesgos</li>"
    recs = "".join(f"<li>{escape(str(x))}</li>" for x in resp.get("recomendaciones", [])) or "<li>Sin recomendaciones</li>"
    frags = "".join(
        f"<li><strong>{escape(str(f.get('doc_id')))}</strong> · {escape(str(f.get('titulo')))}<br>{escape(str(f.get('contenido',''))[:220])}...</li>"
        for f in fragmentos
    ) or "<li>Sin fragmentos recuperados</li>"
    fallback_html = f"<p><strong>Motivo fallback:</strong> {escape(fallback)}</p>" if fallback else ""

    return f"""<!doctype html>
<html lang=\"es\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>Panel Demo RAG V2.1</title>
  <style>
    body {{ margin:0; font-family:'Segoe UI', Tahoma, sans-serif; background:#f3f7fb; color:#11263a; }}
    .wrap {{ max-width:1100px; margin:24px auto; padding:0 16px 24px; }}
    .card {{ background:#fff; border:1px solid #d9e2ee; border-radius:14px; padding:16px; margin-bottom:14px; }}
    .badges {{ display:flex; gap:8px; flex-wrap:wrap; }}
    .badge {{ background:#eaf3ff; border:1px solid #c8d9ee; border-radius:999px; padding:5px 10px; font-weight:600; }}
    .flow {{ display:grid; grid-template-columns:repeat(6,minmax(0,1fr)); gap:8px; }}
    .step {{ border:1px solid #d7e2ef; border-radius:10px; padding:9px; text-align:center; background:#f9fcff; }}
    .grid {{ display:grid; grid-template-columns:1fr 1fr; gap:12px; }}
    ul {{ margin:0.3rem 0 0 1.1rem; }}
    @media (max-width:900px) {{ .grid, .flow {{ grid-template-columns:1fr; }} }}
  </style>
</head>
<body>
  <div class=\"wrap\">
    <div class=\"card\">
      <h1>Laboratorio RAG corporativo local — Demo V2.1</h1>
      <p>Qué demuestra: recuperación local de documentos sintéticos, contexto controlado y análisis LLM opcional con fallback determinista.</p>
      <div class=\"badges\">
        <span class=\"badge\">Proveedor: {escape(str(proveedor))}</span>
        <span class=\"badge\">Modelo: {escape(str(modelo))}</span>
        <span class=\"badge\">Ruta ejecución: {escape(str(ruta))}</span>
      </div>
      {fallback_html}
    </div>

    <div class=\"card\">
      <h2>Flujo visual</h2>
      <div class=\"flow\">
        <div class=\"step\">Documentos</div>
        <div class=\"step\">Recuperación</div>
        <div class=\"step\">Contexto</div>
        <div class=\"step\">LLM/Fallback</div>
        <div class=\"step\">Respuesta</div>
        <div class=\"step\">Evidencia</div>
      </div>
    </div>

    <div class=\"card\">
      <h2>Consulta de ejemplo</h2>
      <p>{escape(consulta)}</p>
    </div>

    <div class=\"card\">
      <h2>Fragmentos recuperados</h2>
      <ul>{frags}</ul>
    </div>

    <div class=\"card\">
      <h2>Respuesta generada</h2>
      <p><strong>Resumen:</strong> {escape(str(resp.get('resumen', 'Sin resumen')))}</p>
      <div class=\"grid\">
        <div>
          <h3>Riesgos</h3>
          <ul>{riesgos}</ul>
        </div>
        <div>
          <h3>Recomendaciones</h3>
          <ul>{recs}</ul>
        </div>
      </div>
    </div>

    <div class=\"card\">
      <h2>Rutas de evidencias</h2>
      <ul>
        <li>evidencias/demo_llm_groq.md</li>
        <li>evidencias/resultado_demo_llm_groq.json</li>
        <li>evidencias/panel_demo.html</li>
        <li>evidencias/interactivas/</li>
      </ul>
      <p>Para probar consultas propias en vivo: ejecutar <code>python scripts/servidor_demo_interactivo.py</code></p>
    </div>
  </div>
</body>
</html>
"""


def main() -> None:
    if not RUTA_RESULTADO_DEMO_LLM.exists():
        raise FileNotFoundError(f"No existe {RUTA_RESULTADO_DEMO_LLM}. Ejecuta antes scripts/demo_llm_groq.py")

    resultado = json.loads(RUTA_RESULTADO_DEMO_LLM.read_text(encoding="utf-8"))
    RUTA_PANEL_DEMO.write_text(_html(resultado), encoding="utf-8")
    print("Panel demo generado")
    print(f"- Archivo: {RUTA_PANEL_DEMO}")


if __name__ == "__main__":
    main()
