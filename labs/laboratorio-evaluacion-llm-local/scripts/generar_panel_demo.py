import argparse
import json
import sys
from html import escape
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))


def _licencia_html() -> str:
    return "<p>Licencia: CC BY-SA 4.0 International. Autoría: Txema Ríos.</p>"


def generar_html(data: dict) -> str:
    resultados = data.get("resultados", [])
    ultimo = resultados[-1] if resultados else {}
    criterios = "".join(f"<li>{escape(k)}: {escape(str(v))}</li>" for k, v in ultimo.get("puntuaciones", {}).items())
    rutas = ["evidencias/resultado_demo_llm_groq.json", "evidencias/demo_llm_groq.md"]
    rutas_html = "".join(f"<li>{escape(r)}</li>" for r in rutas)

    return f"""<!doctype html>
<html lang=\"es\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>Panel Demo V2.1</title>
  <style>
    :root {{ --fondo:#f6f6ef; --panel:#ffffff; --acento:#0f766e; --texto:#1f2937; }}
    body {{ margin:0; font-family:'Trebuchet MS', 'Segoe UI', sans-serif; background:linear-gradient(130deg,#fef3c7,#e0f2fe); color:var(--texto); }}
    .wrap {{ max-width:1100px; margin:20px auto; padding:20px; }}
    .card {{ background:var(--panel); border-radius:16px; padding:18px; margin-bottom:16px; box-shadow:0 8px 24px rgba(0,0,0,0.08); }}
    h1,h2 {{ margin: 0 0 10px; }}
    .badge {{ display:inline-block; padding:6px 10px; background:#ccfbf1; border-radius:20px; margin-right:8px; }}
  </style>
</head>
<body>
  <div class=\"wrap\">
    <div class=\"card\">
      <h1>Laboratorio evaluación LLM local - V2.1</h1>
      <p>Demuestra evaluación reproducible con Groq opcional y fallback local determinista.</p>
      <span class=\"badge\">Proveedor: {escape(str(ultimo.get('proveedor', 'n/a')))}</span>
      <span class=\"badge\">Modelo: {escape(str(ultimo.get('modelo', 'n/a')))}</span>
      <span class=\"badge\">Ruta: {escape(str(ultimo.get('ruta_ejecucion', 'n/a')))}</span>
    </div>
    <div class=\"card\"><h2>Caso evaluado</h2><p>{escape(str(ultimo.get('escenario', 'n/a')))}</p></div>
    <div class=\"card\"><h2>Respuesta candidata</h2><p>{escape(str(ultimo.get('respuesta_candidata', 'n/a')))}</p></div>
    <div class=\"card\"><h2>Criterios de evaluación y puntuaciones</h2><ul>{criterios}</ul></div>
    <div class=\"card\"><h2>Explicación</h2><p>{escape(str(ultimo.get('explicacion', 'n/a')))}</p></div>
    <div class=\"card\"><h2>Trazabilidad y fallback</h2><p>Motivo fallback: {escape(str(ultimo.get('motivo_fallback', 'n/a')))}</p></div>
    <div class=\"card\"><h2>Rutas de evidencia</h2><ul>{rutas_html}</ul></div>
    <div class=\"card\">{_licencia_html()}</div>
  </div>
</body>
</html>"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--entrada", default=str(BASE / "evidencias" / "resultado_demo_llm_groq.json"))
    parser.add_argument("--salida", default=str(BASE / "evidencias" / "panel_demo.html"))
    args = parser.parse_args()

    data = json.loads(Path(args.entrada).read_text(encoding="utf-8-sig"))
    html = generar_html(data)
    salida = Path(args.salida)
    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.write_text(html, encoding="utf-8")
    print(f"Panel generado: {salida}")


if __name__ == "__main__":
    main()
