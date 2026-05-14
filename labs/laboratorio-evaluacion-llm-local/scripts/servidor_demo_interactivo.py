import argparse
import html
import json
import os
import sys
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

BASE = Path(__file__).resolve().parents[1]
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from servicios.evaluacion_llm_v21 import CRITERIOS_DISPONIBLES, cargar_casos_demo, evaluar_respuesta_llm, guardar_evidencia_json

HISTORIAL = []
CASOS = cargar_casos_demo(BASE / "datos" / "casos_demo_llm_v21.json")
CASOS_POR_ID = {c["id"]: c for c in CASOS}
RIESGO_POR_ESCENARIO = {
    "respuesta_inventada": "alucinación o dato no soportado",
    "respuesta_correcta_incompleta": "cobertura insuficiente",
    "riesgo_privacidad": "exposición de datos sensibles",
    "respuesta_ejecutiva_direccion": "calidad ejecutiva y completitud",
    "rag_contexto_insuficiente": "límites de respuesta y falta de evidencia",
}


def _badge_estado_llm() -> str:
    if os.getenv("GROQ_API_KEY", "").strip():
        return "Groq detectado"
    return "Groq no configurado"


def _licencia_md() -> str:
    return (
        "\n---\n\n"
        "## Licencia y Autoría\n"
        "Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.\n"
        "© 2026 - Txema Ríos.\n"
    )


def _guardar_evidencias_interactivas(resultado: dict) -> dict:
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    base = BASE / "evidencias" / "interactivas"
    base.mkdir(parents=True, exist_ok=True)
    ruta_json = base / f"evaluacion_{ts}.json"
    ruta_md = base / f"evaluacion_{ts}.md"
    guardar_evidencia_json(resultado, ruta_json)

    lineas = [
        "# Evidencia interactiva V2.1",
        "",
        f"- Fecha UTC: `{resultado['fecha_utc']}`",
        f"- Escenario: `{resultado['escenario']}`",
        f"- Proveedor: `{resultado['proveedor']}`",
        f"- Modelo: `{resultado['modelo']}`",
        f"- Ruta ejecución: `{resultado['ruta_ejecucion']}`",
        f"- Motivo fallback: `{resultado['motivo_fallback']}`",
        "",
        "## Puntuaciones",
    ]
    for k, v in resultado["puntuaciones"].items():
        lineas.append(f"- {k}: `{v}`")
    lineas.extend([
        "",
        "## Explicación",
        resultado["explicacion"],
        "",
        "## Riesgos",
        "- " + (", ".join(resultado["riesgos"]) if resultado["riesgos"] else "ninguno"),
        "",
        "## Recomendaciones",
        "- " + ("; ".join(resultado["recomendaciones"]) if resultado["recomendaciones"] else "ninguna"),
        _licencia_md(),
    ])
    ruta_md.write_text("\n".join(lineas), encoding="utf-8")
    return {"json": str(ruta_json), "md": str(ruta_md)}


def _estado_inicial() -> dict:
    return {
        "escenario": CASOS[0]["id"],
        "nombre": "",
        "descripcion": "",
        "pregunta": "",
        "contexto_esperado": "",
        "respuesta_candidata": "",
        "criterios": list(CRITERIOS_DISPONIBLES),
        "estado": "Listo",
        "error": "",
        "resultado": None,
        "evidencias": None,
        "fecha": "",
    }


def _cargar_escenario_en_estado(estado: dict, escenario_id: str) -> dict:
    caso = CASOS_POR_ID.get(escenario_id)
    if not caso:
        estado["error"] = f"Error controlado: escenario no encontrado ({escenario_id})."
        estado["estado"] = "Error"
        return estado
    estado["escenario"] = caso["id"]
    estado["nombre"] = caso["nombre"]
    estado["descripcion"] = caso["descripcion"]
    estado["pregunta"] = caso["pregunta"]
    estado["contexto_esperado"] = caso["contexto_esperado"]
    estado["respuesta_candidata"] = caso["respuesta_candidata"]
    estado["criterios"] = caso["criterios"]
    estado["estado"] = "Escenario cargado"
    estado["error"] = ""
    estado["resultado"] = None
    estado["evidencias"] = None
    estado["fecha"] = ""
    return estado


def _render_dashboard(estado: dict) -> str:
    opciones = []
    for c in CASOS:
        sel = " selected" if c["id"] == estado["escenario"] else ""
        opciones.append(f"<option value='{html.escape(c['id'])}'{sel}>{html.escape(c['nombre'])}</option>")

    checks = []
    selected = set(estado["criterios"])
    for crit in CRITERIOS_DISPONIBLES:
        checked = " checked" if crit in selected else ""
        checks.append(f"<label><input type='checkbox' name='criterios' value='{crit}'{checked}> {crit}</label>")

    res = estado.get("resultado") or {}
    puntuaciones = json.dumps(res.get("puntuaciones", {}), ensure_ascii=False, indent=2)
    riesgos = "\n".join(res.get("riesgos", [])) if res.get("riesgos") else ""
    recomendaciones = "\n".join(res.get("recomendaciones", [])) if res.get("recomendaciones") else ""
    trazabilidad = json.dumps({
        "proveedor": res.get("proveedor", ""),
        "modelo": res.get("modelo", ""),
        "ruta_ejecucion": res.get("ruta_ejecucion", ""),
        "motivo_fallback": res.get("motivo_fallback", ""),
    }, ensure_ascii=False, indent=2)

    historial_text = json.dumps(HISTORIAL[-10:], ensure_ascii=False, indent=2)
    evidencias_text = json.dumps(estado.get("evidencias") or {}, ensure_ascii=False, indent=2)
    riesgo_activo = RIESGO_POR_ESCENARIO.get(estado.get("escenario", ""), "riesgo no clasificado")

    return f"""<!doctype html>
<html lang='es'>
<head>
<meta charset='utf-8'>
<meta name='viewport' content='width=device-width, initial-scale=1'>
<title>Dashboard interactivo V2.1</title>
<style>
:root {{ --fondo:#f5efe2; --panel:#fff; --acento:#0f766e; --texto:#111827; --ok:#166534; --err:#991b1b; }}
body {{ margin:0; font-family:Verdana,Segoe UI,sans-serif; background:linear-gradient(140deg,#fef3c7,#dbeafe); color:var(--texto); }}
.wrap {{ max-width:1200px; margin:14px auto; padding:12px; display:grid; grid-template-columns:1fr 1fr; gap:12px; }}
.card {{ background:var(--panel); border-radius:14px; padding:14px; box-shadow:0 8px 24px rgba(0,0,0,.08); }}
.full {{ grid-column:1 / -1; }}
textarea,select {{ width:100%; min-height:88px; }}
button {{ background:var(--acento); color:#fff; border:0; border-radius:8px; padding:9px 12px; cursor:pointer; }}
.small {{ font-size:12px; white-space:pre-wrap; }}
.badge {{ display:inline-block; border-radius:999px; padding:4px 10px; background:#ccfbf1; }}
.estado {{ font-weight:bold; color:var(--ok); }}
.error {{ font-weight:bold; color:var(--err); }}
.info {{ background:#ecfeff; border-left:4px solid #0891b2; padding:10px; border-radius:8px; }}
</style>
</head>
<body>
<div class='wrap'>
  <div class='card full'>
    <h1>Dashboard interactivo V2.1</h1>
    <p class='badge'>{html.escape(_badge_estado_llm())}</p>
    <p class='estado'>Estado: {html.escape(estado['estado'])}</p>
    <p>{'Escenario cargado: ' + html.escape(estado['nombre']) if estado.get('nombre') else ''}</p>
    <p class='error'>{html.escape(estado['error'])}</p>
  </div>

  <div class='card full'>
    <h2>Para qué sirve este laboratorio</h2>
    <p>Este laboratorio permite evaluar respuestas generadas por LLMs antes de usarlas en un contexto empresarial. Sirve para detectar respuestas inventadas, incompletas, inseguras, poco trazables o no justificadas por el contexto disponible.</p>
  </div>

  <div class='card'>
    <h2>Qué demuestra técnicamente</h2>
    <ul>
      <li>evaluación local de respuestas LLM;</li>
      <li>detección de alucinaciones o datos no soportados por el contexto;</li>
      <li>análisis de cobertura, precisión, seguridad, consistencia y trazabilidad;</li>
      <li>uso opcional de Groq para evaluación asistida;</li>
      <li>fallback local determinista sin dependencia obligatoria de cloud;</li>
      <li>generación de evidencias JSON/Markdown;</li>
      <li>dashboard interactivo reproducible para pruebas.</li>
    </ul>
  </div>

  <div class='card'>
    <h2>Cómo lo usaría una empresa</h2>
    <ul>
      <li>revisar respuestas de un sistema RAG antes de mostrarlas a usuarios;</li>
      <li>detectar si una respuesta inventa cifras, obligaciones o datos;</li>
      <li>comprobar si una respuesta contiene riesgos de privacidad;</li>
      <li>comparar respuestas candidatas antes de incorporarlas a un asistente IA;</li>
      <li>dejar evidencias de evaluación para auditoría técnica.</li>
    </ul>
  </div>

  <div class='card'>
    <h2>1. Caso a evaluar</h2>
    <form method='POST' action='/cargar'>
      <label>Escenario</label>
      <select name='escenario'>
        {''.join(opciones)}
      </select>
      <button type='submit'>Cargar escenario</button>
    </form>

    <p class='info'>Este caso prueba si el evaluador detecta: {html.escape(riesgo_activo)}</p>

    <form method='POST' action='/evaluar'>
      <input type='hidden' name='escenario' value='{html.escape(estado['escenario'])}'>
      <label>Pregunta</label>
      <textarea name='pregunta'>{html.escape(estado['pregunta'])}</textarea>
      <label>Contexto esperado</label>
      <textarea name='contexto_esperado'>{html.escape(estado['contexto_esperado'])}</textarea>
      <label>Respuesta candidata</label>
      <textarea name='respuesta_candidata'>{html.escape(estado['respuesta_candidata'])}</textarea>
      <p>{html.escape(estado.get('descripcion', ''))}</p>
      <h3>Criterios</h3>
      <div>{''.join(checks)}</div>
      <label><input type='checkbox' name='forzar_fallback' value='1'> Forzar fallback local</label>
      <br><br>
      <button type='submit'>Evaluar respuesta</button>
    </form>
  </div>

  <div class='card'>
    <h2>2. Evaluación generada</h2>
    <h3>Puntuaciones</h3><pre id='out_puntuaciones' class='small'>{html.escape(puntuaciones)}</pre>
    <div class='info'>
      <strong>Cómo interpretar las puntuaciones</strong>
      <p>valores altos indican mejor alineación con el contexto y los criterios; valores bajos alertan de riesgo, falta de cobertura o invención; la trazabilidad indica si la evaluación fue generada por Groq o fallback local.</p>
    </div>
    <h3>Explicación</h3><pre id='out_explicacion' class='small'>{html.escape(res.get('explicacion', ''))}</pre>
    <h3>Riesgos</h3><pre id='out_riesgos' class='small'>{html.escape(riesgos)}</pre>
    <h3>Recomendaciones</h3><pre id='out_recomendaciones' class='small'>{html.escape(recomendaciones)}</pre>
    <h3>Trazabilidad</h3><pre id='out_trazabilidad' class='small'>{html.escape(trazabilidad)}</pre>
    <h3>Fecha/hora</h3><pre id='out_fecha' class='small'>{html.escape(estado.get('fecha', ''))}</pre>
    <h3>Rutas de evidencia</h3><pre id='out_evidencias' class='small'>{html.escape(evidencias_text)}</pre>
    <button type='button' onclick="copiar('out_puntuaciones')">Copiar puntuaciones</button>
    <button type='button' onclick="copiar('out_trazabilidad')">Copiar trazabilidad</button>
    <button type='button' onclick="copiar('out_evidencias')">Copiar rutas evidencia</button>
  </div>

  <div class='card full'>
    <h2>3. Evidencias generadas</h2>
    <pre class='small'>{html.escape(historial_text)}</pre>
  </div>
</div>
<script>
function copiar(id) {{
  const el = document.getElementById(id);
  if (el) navigator.clipboard.writeText(el.textContent || '');
}}
</script>
</body>
</html>"""


def _parse_form(handler: BaseHTTPRequestHandler) -> dict[str, list[str]]:
    length = int(handler.headers.get("Content-Length", "0"))
    raw = handler.rfile.read(length).decode("utf-8")
    return parse_qs(raw, keep_blank_values=True)


def _first(form: dict[str, list[str]], key: str, default: str = "") -> str:
    vals = form.get(key)
    if not vals:
        return default
    return vals[0]


def _handle_get_root() -> str:
    estado = _estado_inicial()
    return _render_dashboard(estado)


def _handle_post_cargar(form: dict[str, list[str]]) -> str:
    estado = _estado_inicial()
    escenario = _first(form, "escenario", estado["escenario"])
    return _render_dashboard(_cargar_escenario_en_estado(estado, escenario))


def _handle_post_evaluar(form: dict[str, list[str]]) -> str:
    estado = _estado_inicial()
    try:
        estado["escenario"] = _first(form, "escenario", estado["escenario"])
        estado["pregunta"] = _first(form, "pregunta", "")
        estado["contexto_esperado"] = _first(form, "contexto_esperado", "")
        estado["respuesta_candidata"] = _first(form, "respuesta_candidata", "")
        estado["criterios"] = form.get("criterios", list(CRITERIOS_DISPONIBLES))
        caso = CASOS_POR_ID.get(estado["escenario"])
        if caso:
            estado["nombre"] = caso["nombre"]
            estado["descripcion"] = caso["descripcion"]

        forzar = _first(form, "forzar_fallback", "") in {"1", "on", "true"}
        resultado = evaluar_respuesta_llm(
            escenario=estado["escenario"],
            pregunta=estado["pregunta"],
            contexto=estado["contexto_esperado"],
            respuesta_candidata=estado["respuesta_candidata"],
            criterios=estado["criterios"],
            forzar_fallback_local=forzar,
        )
        evidencias = _guardar_evidencias_interactivas(resultado)
        estado["resultado"] = resultado
        estado["evidencias"] = evidencias
        estado["fecha"] = resultado.get("fecha_utc", "")
        estado["estado"] = "Evaluación completada"
        HISTORIAL.append({
            "fecha_utc": resultado.get("fecha_utc", ""),
            "escenario": estado["escenario"],
            "proveedor": resultado.get("proveedor", ""),
            "modelo": resultado.get("modelo", ""),
            "ruta_ejecucion": resultado.get("ruta_ejecucion", ""),
            "evidencias": evidencias,
        })
    except Exception as exc:  # noqa: BLE001
        estado["estado"] = "Error"
        estado["error"] = f"Error controlado: {type(exc).__name__}."
    return _render_dashboard(estado)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if urlparse(self.path).path == "/":
            body = _handle_get_root().encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        path = urlparse(self.path).path
        form = _parse_form(self)
        if path == "/cargar":
            body = _handle_post_cargar(form).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if path == "/evaluar":
            body = _handle_post_evaluar(form).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        self.send_response(404)
        self.end_headers()


def ejecutar_self_test() -> int:
    html_get = _handle_get_root()
    if "Dashboard interactivo V2.1" not in html_get or "<select name='escenario'>" not in html_get:
        print("SELF_TEST_FAIL: GET / no renderiza selector")
        return 1

    html_cargar = _handle_post_cargar({"escenario": ["respuesta_correcta_incompleta"]})
    bloques_cargar = [
        "Escenario cargado",
        "Resume la estrategia comercial para dirección.",
        "Objetivos: crecimiento B2B",
        "La estrategia prioriza crecimiento B2B",
    ]
    if any(b not in html_cargar for b in bloques_cargar):
        print("SELF_TEST_FAIL: POST /cargar no rellena campos")
        return 1

    html_eval = _handle_post_evaluar({
        "escenario": ["respuesta_correcta_incompleta"],
        "pregunta": ["Resume la estrategia comercial para dirección."],
        "contexto_esperado": ["Objetivos: crecimiento B2B, mejora de margen y expansión regional. Riesgos: churn y presión competitiva."],
        "respuesta_candidata": ["La estrategia prioriza crecimiento B2B y mejora de margen."],
        "criterios": ["relevancia", "precision", "cobertura"],
        "forzar_fallback": ["1"],
    })
    bloques_eval = ["Evaluación completada", "Puntuaciones", "Explicación", "Riesgos", "Recomendaciones", "Trazabilidad", "fallback_local"]
    if any(b not in html_eval for b in bloques_eval):
        print("SELF_TEST_FAIL: POST /evaluar no completa salida")
        return 1

    if not HISTORIAL or not HISTORIAL[-1].get("evidencias"):
        print("SELF_TEST_FAIL: no se registraron evidencias")
        return 1
    ev = HISTORIAL[-1]["evidencias"]
    if not Path(ev["json"]).exists() or not Path(ev["md"]).exists():
        print("SELF_TEST_FAIL: no existen archivos de evidencia")
        return 1

    print("SELF_TEST_OK")
    print(f"Evidencia JSON: {ev['json']}")
    print(f"Evidencia MD: {ev['md']}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8768)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        return ejecutar_self_test()

    if args.host != "127.0.0.1":
        print("Por seguridad, solo se permite 127.0.0.1")
        return 1

    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"Servidor demo interactivo: http://{args.host}:{args.port}")
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
