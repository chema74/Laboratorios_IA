import json
import sys
from html import escape
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from app.config import RUTA_PANEL_DEMO, RUTA_RESULTADO_DEMO_LLM


def _html(resultado: dict) -> str:
    def _li(items: list[str]) -> str:
        return "".join(f"<li>{escape(str(i))}</li>" for i in items) or "<li>Sin datos</li>"

    def _texto_lista(items: list[str]) -> str:
        limpios = [str(i).strip() for i in items if str(i).strip()]
        return ", ".join(limpios) if limpios else "Sin datos"

    llm = resultado.get("analisis_llm", {})
    respuesta = llm.get("respuesta", {})
    trazas_llm = llm.get("trazabilidad", {})
    motor = resultado.get("motor_privacidad", {})
    metadata = resultado.get("metadata", {})

    riesgo = motor.get("evaluacion_exposicion", {}).get("nivel_riesgo", "desconocido")
    score = motor.get("evaluacion_exposicion", {}).get("puntuacion", 0)
    modelo = llm.get("modelo", trazas_llm.get("groq_model", "desconocido"))
    ruta_ejecucion = trazas_llm.get("ruta_ejecucion", "indefinida")
    proveedor = llm.get("proveedor", "desconocido")
    fecha = metadata.get("fecha_utc", "no disponible")

    analisis_casos = motor.get("analisis_casos", [])
    primer_caso = analisis_casos[0] if analisis_casos else {}
    detecciones = primer_caso.get("detecciones", [])

    tipos_pii = {
        str(d.get("tipo", "")).strip().lower()
        for c in analisis_casos
        for d in c.get("detecciones", [])
        if d.get("tipo")
    }
    if motor.get("prompts_minimizados"):
        tipos_pii.add("contexto sensible de negocio")
    orden = ["nombre", "email", "telefono", "identificador", "contexto sensible de negocio"]
    tipos_ordenados = [t for t in orden if t in tipos_pii] + sorted(t for t in tipos_pii if t not in orden)

    muestra_original = _texto_lista([d.get("valor", "") for d in detecciones[:6]])
    muestra_minimizada = primer_caso.get("anonimizacion", {}).get("texto_anonimizado", "Sin datos minimizados")

    riesgos = _li(respuesta.get("riesgos", []))
    recomendaciones = _li(respuesta.get("recomendaciones", []))
    pii_detectada = _li(tipos_ordenados)

    motivo_fallback = llm.get("motivo_fallback", "")
    motivo_html = f"<p><strong>Motivo fallback:</strong> {escape(str(motivo_fallback))}</p>" if motivo_fallback else ""

    return f"""<!doctype html>
<html lang=\"es\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>Laboratorio de privacidad de datos IA — Demo V2.1</title>
  <style>
    :root {{ --fondo:#f3f6fa; --card:#ffffff; --txt:#15243a; --muted:#4a6078; --acento:#0b5f99; --borde:#d4deea; --ok:#106f58; --warn:#a24f00; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; font-family:'Segoe UI', Tahoma, sans-serif; background:linear-gradient(140deg,#eaf1fb,#f8fcf7); color:var(--txt); }}
    .wrap {{ max-width:1120px; margin:24px auto; padding:0 16px 24px; }}
    .card {{ background:var(--card); border:1px solid var(--borde); border-radius:14px; padding:18px; margin-bottom:14px; box-shadow:0 1px 0 rgba(15,35,60,.03); }}
    h1,h2,h3 {{ margin-top:0; }}
    h1 {{ font-size:1.72rem; margin-bottom:0.2rem; }}
    h2 {{ font-size:1.2rem; color:#133f61; margin-bottom:0.5rem; }}
    h3 {{ font-size:1rem; color:#17395b; margin-bottom:0.4rem; }}
    .sub {{ color:var(--muted); margin-bottom:10px; }}
    .badges {{ display:flex; flex-wrap:wrap; gap:8px; margin-top:12px; }}
    .badge {{ display:inline-block; border:1px solid #cbd9e8; background:#f5f9ff; color:#0d395d; border-radius:999px; padding:5px 10px; font-weight:600; font-size:0.86rem; }}
    .grid2 {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:12px; }}
    .pipe {{ display:grid; grid-template-columns:repeat(6,minmax(0,1fr)); gap:8px; }}
    .step {{ border:1px solid var(--borde); background:#fbfdff; border-radius:10px; padding:10px; font-size:0.92rem; text-align:center; }}
    .arrow::after {{ content:'→'; margin-left:7px; color:#6885a2; }}
    p {{ margin:0.35rem 0; }}
    ul {{ margin:0.45rem 0 0 1.1rem; padding:0; }}
    .pre {{ font-family:Consolas, monospace; background:#f4f8fd; border:1px solid #dce6f2; border-radius:10px; padding:10px; white-space:pre-wrap; word-break:break-word; }}
    .ok {{ color:var(--ok); font-weight:600; }}
    .warn {{ color:var(--warn); font-weight:600; }}
    code {{ background:#f1f5f9; border:1px solid #e1e8f0; border-radius:6px; padding:1px 5px; }}
    @media (max-width: 980px) {{ .pipe {{ grid-template-columns:repeat(3,minmax(0,1fr)); }} }}
    @media (max-width: 760px) {{ .grid2, .pipe {{ grid-template-columns:1fr; }} .arrow::after {{ content:''; }} }}
  </style>
</head>
<body>
  <div class=\"wrap\">
    <div class=\"card\">
      <h1>Laboratorio de privacidad de datos IA — Demo V2.1</h1>
      <p class=\"sub\">Privacidad, minimización y análisis LLM opcional antes de enviar datos sensibles a IA</p>
      <div class=\"badges\">
        <span class=\"badge\">Proveedor LLM: {escape(str(proveedor))}</span>
        <span class=\"badge\">Modelo: {escape(str(modelo))}</span>
        <span class=\"badge\">Ruta de ejecución: {escape(str(ruta_ejecucion))}</span>
        <span class=\"badge\">Riesgo global: {escape(str(riesgo))} (score={escape(str(score))})</span>
        <span class=\"badge\">Fecha: {escape(str(fecha))}</span>
      </div>
    </div>

    <div class=\"card\">
      <h2>Qué demuestra esta demo</h2>
      <p>El laboratorio recibe datos sintéticos con PII para simular escenarios reales sin usar datos personales.</p>
      <p>Detecta exposición, minimiza y anonimiza contexto antes de la capa LLM, reduciendo superficie de riesgo.</p>
      <p>Con Groq disponible genera análisis remoto; sin clave o ante error mantiene fallback local y evidencias reproducibles.</p>
    </div>

    <div class=\"card\">
      <h2>Flujo de privacidad (pipeline)</h2>
      <div class=\"pipe\">
        <div class=\"step arrow\">Datos sensibles</div>
        <div class=\"step arrow\">Detección PII</div>
        <div class=\"step arrow\">Minimización</div>
        <div class=\"step arrow\">Análisis Groq (opcional)</div>
        <div class=\"step arrow\">Recomendaciones</div>
        <div class=\"step\">Evidencias</div>
      </div>
    </div>

    <div class=\"card\">
      <h2>Comparativa antes/después</h2>
      <div class=\"grid2\">
        <div>
          <h3>Entrada original con PII sintética</h3>
          <div class=\"pre\">{escape(muestra_original)}</div>
        </div>
        <div>
          <h3>Versión minimizada para IA</h3>
          <div class=\"pre ok\">{escape(muestra_minimizada)}</div>
        </div>
      </div>
    </div>

    <div class=\"card\">
      <h2>PII detectada o simulada</h2>
      <ul>{pii_detectada}</ul>
    </div>

    <div class=\"card\">
      <h2>Resultado del análisis LLM</h2>
      <p><strong>Resumen ejecutivo:</strong> {escape(str(respuesta.get('resumen', 'Sin resumen')))}</p>
      <p><strong>Nivel de riesgo global:</strong> <span class=\"warn\">{escape(str(riesgo))}</span></p>
      <h3>Riesgos detectados</h3>
      <ul>{riesgos}</ul>
      <h3>Recomendaciones</h3>
      <ul>{recomendaciones}</ul>
    </div>

    <div class=\"card\">
      <h2>Bloque de trazabilidad</h2>
      <p><strong>Proveedor utilizado:</strong> {escape(str(proveedor))}</p>
      <p><strong>Modelo:</strong> {escape(str(modelo))}</p>
      <p><strong>Ruta de ejecución:</strong> {escape(str(ruta_ejecucion))}</p>
      {motivo_html}
      <p><strong>Archivo JSON:</strong> <code>evidencias/resultado_demo_llm_groq.json</code></p>
      <p><strong>Archivo Markdown:</strong> <code>evidencias/demo_llm_groq.md</code></p>
    </div>

    <div class=\"card\">
      <h2>Por qué esto importa en empresa</h2>
      <ul>
        <li>Evita enviar datos personales innecesarios a un LLM.</li>
        <li>Permite revisar salidas antes de compartirlas o publicarlas.</li>
        <li>Separa motor local de privacidad y capa LLM opcional.</li>
        <li>Funciona sin API key mediante fallback local determinista.</li>
        <li>Genera evidencias reproducibles para auditoría técnica.</li>
      </ul>
    </div>

    <div class=\"card\">
      <h2>Archivos de evidencia</h2>
      <ul>
        <li><code>evidencias/demo_llm_groq.md</code></li>
        <li><code>evidencias/resultado_demo_llm_groq.json</code></li>
        <li><code>evidencias/panel_demo.html</code></li>
      </ul>
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
