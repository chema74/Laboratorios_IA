import argparse
import json
import os
import re
import sys
from datetime import UTC, datetime
from html import escape
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs

BASE = Path(__file__).resolve().parents[1]
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from app.config import RUTA_EVIDENCIAS
from privacidad.anonimizador import anonimizar_texto
from privacidad.detector_pii import detectar_pii
from privacidad.minimizador_contexto import minimizar_contexto
from servicios.analisis_llm import analizar_privacidad_llm

HOST = "127.0.0.1"
PORT = 8766

CASOS_EJEMPLO = {
    "cliente": "Cliente NombreDemo Uno con email cliente.demo@empresa.local, telefono 612345678 e identificador A12345678Z para revision de contrato.",
    "empleado": "Empleado NombreDemo Dos del area de rrhh con email empleado.rrhh@empresa.local, telefono 699887766 y observacion de baja medica en expediente.",
    "lead": "Lead comercial NombreDemo Tres contacto lead.comercial@demo.local telefono 688776655 interesado en propuesta enterprise para integracion IA.",
    "pyme": "Incidencia financiera de PYME: NombreDemo Cuatro reporta tension de tesoreria, email finanzas.pyme@demo.local, telefono 677665544, identificador B87654321X.",
}

PATRON_CONTEXTO_SENSIBLE = re.compile(
    r"\b(rrhh|baja medica|tesoreria|financier[ao]|incidencia|expediente|contrato|nomina|sancion)\b",
    re.IGNORECASE,
)


def _bool_form(valor: str | None) -> bool:
    if valor is None:
        return False
    return valor.strip().lower() in {"1", "true", "on", "yes", "si"}


def _detectar_contexto_sensible(texto: str) -> bool:
    return bool(PATRON_CONTEXTO_SENSIBLE.search(texto or ""))


def analizar_texto_interactivo(
    texto_original: str,
    usar_groq: bool,
    forzar_fallback_local: bool,
    api_key: str | None = None,
    opener=None,
) -> dict:
    texto = (texto_original or "").strip()
    if not texto:
        raise ValueError("Debes proporcionar un texto para analizar")

    nombres = sorted({m.group(0) for m in re.finditer(r"\bNombreDemo\s+[A-Za-zÁÉÍÓÚáéíóú]+\b", texto)})
    pii = detectar_pii(texto, nombres_marcados=nombres)
    if _detectar_contexto_sensible(texto):
        pii.append({"tipo": "contexto sensible de negocio", "valor": "detectado", "inicio": 0, "severidad": "media"})

    anon = anonimizar_texto(texto, nombres_marcados=nombres)
    min_ctx = minimizar_contexto(
        {
            "caso_uso": "demo_interactiva",
            "objetivo": "analisis_privacidad",
            "texto": anon.get("texto_anonimizado", texto),
            "metadata_descartable": "no_enviar",
        }
    )

    riesgo = "alto" if len(pii) >= 4 else "medio" if len(pii) >= 2 else "bajo"
    score = min(20, len(pii) * 3 + (3 if _detectar_contexto_sensible(texto) else 0))

    resultado_motor = {
        "analisis_casos": [
            {
                "id": "INTERACTIVO-001",
                "detecciones": pii,
                "anonimizacion": anon,
            }
        ],
        "prompts_minimizados": [min_ctx],
        "validacion_salidas": [{"estado": "revisar" if pii else "segura", "hallazgos": pii}],
        "evaluacion_exposicion": {"nivel_riesgo": riesgo, "puntuacion": score},
    }

    entorno = dict(os.environ)
    if forzar_fallback_local or not usar_groq:
        entorno["FORZAR_FALLBACK_LOCAL"] = "1"
    else:
        entorno.pop("FORZAR_FALLBACK_LOCAL", None)

    clave = api_key if api_key is not None else (entorno.get("GROQ_API_KEY") if usar_groq and not forzar_fallback_local else None)

    kwargs = {}
    if opener is not None:
        kwargs["opener"] = opener

    analisis_llm = analizar_privacidad_llm(
        resultado_motor,
        api_key=clave,
        cargar_env=False,
        entorno=entorno,
        **kwargs,
    )

    respuesta = analisis_llm.get("respuesta", {})
    trazas = analisis_llm.get("trazabilidad", {})

    return {
        "fecha": datetime.now(UTC).isoformat(),
        "texto_original": texto,
        "texto_minimizado": min_ctx.get("texto_minimizado", ""),
        "pii_detectada": pii,
        "analisis_llm": analisis_llm,
        "proveedor": analisis_llm.get("proveedor", "desconocido"),
        "modelo": analisis_llm.get("modelo", trazas.get("groq_model", "desconocido")),
        "ruta_ejecucion": trazas.get("ruta_ejecucion", "indefinida"),
        "motivo_fallback": analisis_llm.get("motivo_fallback", ""),
        "resumen": respuesta.get("resumen", "Sin resumen"),
        "riesgos": respuesta.get("riesgos", []),
        "recomendaciones": respuesta.get("recomendaciones", []),
        "resultado_motor": resultado_motor,
    }


def _render_markdown_evidencia(resultado: dict, json_path: Path) -> str:
    pii_tipos = sorted({d.get("tipo", "desconocido") for d in resultado.get("pii_detectada", [])})
    lineas = [
        "# Evidencia Demo Interactiva V2.1",
        "",
        f"- Fecha UTC: {resultado.get('fecha', 'n/a')}",
        f"- Proveedor: {resultado.get('proveedor', 'desconocido')}",
        f"- Modelo: {resultado.get('modelo', 'desconocido')}",
        f"- Ruta de ejecución: {resultado.get('ruta_ejecucion', 'indefinida')}",
        f"- JSON asociado: {json_path}",
        "",
        "## Entrada original",
        resultado.get("texto_original", ""),
        "",
        "## Texto minimizado",
        resultado.get("texto_minimizado", ""),
        "",
        "## PII detectada",
    ]
    for t in pii_tipos:
        lineas.append(f"- {t}")

    lineas.extend([
        "",
        "## Resumen ejecutivo",
        resultado.get("resumen", "Sin resumen"),
        "",
        "## Riesgos",
    ])
    for r in resultado.get("riesgos", []):
        lineas.append(f"- {r}")

    lineas.extend(["", "## Recomendaciones"])
    for rec in resultado.get("recomendaciones", []):
        lineas.append(f"- {rec}")

    motivo = resultado.get("motivo_fallback", "")
    if motivo:
        lineas.extend(["", "## Motivo fallback", motivo])

    lineas.extend([
        "",
        "## Licencia y Autoría",
        "Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.",
        "",
        "© 2026 – Txema Ríos.",
    ])
    return "\n".join(lineas)


def guardar_evidencias_interactivas(resultado: dict, carpeta: Path | None = None) -> dict:
    destino = carpeta or (RUTA_EVIDENCIAS / "interactivas")
    destino.mkdir(parents=True, exist_ok=True)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    ruta_json = destino / f"{ts}_resultado.json"
    ruta_md = destino / f"{ts}_informe.md"

    payload = {
        "fecha": resultado.get("fecha"),
        "texto_original": resultado.get("texto_original"),
        "texto_minimizado": resultado.get("texto_minimizado"),
        "pii_detectada": resultado.get("pii_detectada", []),
        "proveedor": resultado.get("proveedor"),
        "modelo": resultado.get("modelo"),
        "ruta_ejecucion": resultado.get("ruta_ejecucion"),
        "motivo_fallback": resultado.get("motivo_fallback", ""),
        "resumen": resultado.get("resumen"),
        "riesgos": resultado.get("riesgos", []),
        "recomendaciones": resultado.get("recomendaciones", []),
    }
    ruta_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    ruta_md.write_text(_render_markdown_evidencia(resultado, ruta_json), encoding="utf-8")
    return {"json": ruta_json, "markdown": ruta_md}


def _opciones_casos_html() -> str:
    opciones = ["<option value=''>-- Selecciona un caso --</option>"]
    for clave, texto in CASOS_EJEMPLO.items():
        opciones.append(f"<option value=\"{escape(clave)}\">{escape(clave.title())}: {escape(texto[:72])}...</option>")
    return "\n".join(opciones)


def _render_html(resultado: dict | None = None, mensaje_error: str = "") -> str:
    bloque_resultado = ""
    if resultado:
        pii_tipos = sorted({d.get("tipo", "desconocido") for d in resultado.get("pii_detectada", [])})
        trazas = resultado.get("analisis_llm", {}).get("trazabilidad", {})
        riesgos = "".join(f"<li>{escape(str(r))}</li>" for r in resultado.get("riesgos", [])) or "<li>Sin riesgos</li>"
        recomendaciones = "".join(f"<li>{escape(str(r))}</li>" for r in resultado.get("recomendaciones", [])) or "<li>Sin recomendaciones</li>"
        motivo = resultado.get("motivo_fallback")
        motivo_html = f"<p><strong>Motivo fallback:</strong> {escape(str(motivo))}</p>" if motivo else ""

        evidencias = resultado.get("evidencias", {})
        bloque_resultado = f"""
        <section class=\"card\">
          <h2>Resultado del análisis</h2>
          <p><strong>Entrada original:</strong></p>
          <pre>{escape(resultado.get('texto_original', ''))}</pre>
          <p><strong>PII detectada:</strong> {escape(', '.join(pii_tipos) if pii_tipos else 'Sin PII detectada')}</p>
          <p><strong>Versión minimizada:</strong></p>
          <pre>{escape(resultado.get('texto_minimizado', ''))}</pre>
          <p><strong>Resumen ejecutivo:</strong> {escape(str(resultado.get('resumen', 'Sin resumen')))}</p>
          <h3>Riesgos</h3>
          <ul>{riesgos}</ul>
          <h3>Recomendaciones</h3>
          <ul>{recomendaciones}</ul>
          <h3>Trazabilidad LLM</h3>
          <p><strong>Proveedor:</strong> {escape(str(resultado.get('proveedor', 'desconocido')))}</p>
          <p><strong>Modelo:</strong> {escape(str(resultado.get('modelo', 'desconocido')))}</p>
          <p><strong>Ruta ejecución:</strong> {escape(str(resultado.get('ruta_ejecucion', 'indefinida')))}</p>
          {motivo_html}
          <p><strong>Traza completa:</strong> {escape(json.dumps(trazas, ensure_ascii=False))}</p>
          <h3>Evidencias generadas</h3>
          <ul>
            <li>{escape(str(evidencias.get('json', 'n/a')))}</li>
            <li>{escape(str(evidencias.get('markdown', 'n/a')))}</li>
            <li>Panel resumen estático: evidencias/panel_demo.html</li>
          </ul>
        </section>
        """

    error_html = f"<p class='error'>{escape(mensaje_error)}</p>" if mensaje_error else ""
    groq_disponible = "Sí" if os.getenv("GROQ_API_KEY") else "No"

    return f"""<!doctype html>
<html lang=\"es\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>Laboratorio de privacidad de datos IA — Demo interactiva V2.1</title>
  <style>
    body {{ font-family: 'Segoe UI', Tahoma, sans-serif; margin:0; background:#f2f6fb; color:#13253a; }}
    .wrap {{ max-width:1060px; margin:20px auto; padding:0 16px 24px; }}
    .card {{ background:#fff; border:1px solid #d9e3ef; border-radius:12px; padding:16px; margin-bottom:14px; }}
    h1,h2,h3 {{ margin-top:0; }}
    .muted {{ color:#49617a; }}
    label {{ display:block; margin-top:10px; font-weight:600; }}
    textarea, select {{ width:100%; padding:10px; border:1px solid #c9d7e7; border-radius:8px; font-family:inherit; }}
    textarea {{ min-height:130px; }}
    .row {{ display:grid; grid-template-columns:1fr 1fr; gap:10px; }}
    .checks {{ margin-top:10px; display:flex; gap:14px; flex-wrap:wrap; }}
    button {{ margin-top:12px; background:#0a5f98; color:#fff; border:none; border-radius:8px; padding:10px 14px; font-weight:700; cursor:pointer; }}
    pre {{ white-space:pre-wrap; word-break:break-word; background:#f6f9fd; border:1px solid #dbe5f1; border-radius:8px; padding:10px; }}
    .error {{ color:#9a2f1a; font-weight:700; }}
    @media (max-width: 800px) {{ .row {{ grid-template-columns:1fr; }} }}
  </style>
</head>
<body>
  <div class=\"wrap\">
    <section class=\"card\">
      <h1>Laboratorio de privacidad de datos IA — Demo interactiva V2.1</h1>
      <p class=\"muted\">Demostración local para reclutadores y clientes: analiza textos sintéticos con PII, minimiza antes de IA y genera evidencias por ejecución.</p>
      <p class=\"muted\"><strong>Groq API key detectada:</strong> {groq_disponible}</p>
      {error_html}
      <form method=\"post\" action=\"/analizar\">
        <label for=\"caso\">Caso de ejemplo</label>
        <select id=\"caso\" name=\"caso\">{_opciones_casos_html()}</select>

        <label for=\"texto\">Texto a analizar (sintético)</label>
        <textarea id=\"texto\" name=\"texto\" placeholder=\"Pega aquí un texto sintético con posibles datos personales...\"></textarea>

        <div class=\"checks\">
          <label><input type=\"checkbox\" name=\"usar_groq\" value=\"1\" checked /> Usar Groq si hay GROQ_API_KEY</label>
          <label><input type=\"checkbox\" name=\"forzar_fallback\" value=\"1\" /> Forzar fallback local</label>
        </div>

        <button type=\"submit\">Analizar privacidad</button>
      </form>
    </section>
    {bloque_resultado}
  </div>
</body>
</html>
"""


class DemoHandler(BaseHTTPRequestHandler):
    def _responder_html(self, html: str, status: int = 200) -> None:
        data = html.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:
        if self.path in {"/", "/index.html"}:
            self._responder_html(_render_html())
            return
        self._responder_html(_render_html(mensaje_error="Ruta no encontrada"), status=404)

    def do_POST(self) -> None:
        if self.path != "/analizar":
            self._responder_html(_render_html(mensaje_error="Ruta POST no válida"), status=404)
            return

        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length).decode("utf-8")
        form = parse_qs(body)

        caso = (form.get("caso", [""])[0] or "").strip()
        texto_form = (form.get("texto", [""])[0] or "").strip()
        usar_groq = _bool_form(form.get("usar_groq", [None])[0])
        forzar_fallback = _bool_form(form.get("forzar_fallback", [None])[0])

        texto = texto_form or CASOS_EJEMPLO.get(caso, "")

        try:
            resultado = analizar_texto_interactivo(
                texto_original=texto,
                usar_groq=usar_groq,
                forzar_fallback_local=forzar_fallback,
            )
            evidencias = guardar_evidencias_interactivas(resultado)
            resultado["evidencias"] = {"json": str(evidencias["json"]), "markdown": str(evidencias["markdown"])}
            self._responder_html(_render_html(resultado=resultado))
        except Exception as exc:
            self._responder_html(_render_html(mensaje_error=f"Error en análisis: {type(exc).__name__}: {exc}"), status=400)


def ejecutar_self_test() -> None:
    texto = CASOS_EJEMPLO["cliente"]
    resultado = analizar_texto_interactivo(
        texto_original=texto,
        usar_groq=False,
        forzar_fallback_local=True,
    )
    evidencias = guardar_evidencias_interactivas(resultado)

    assert resultado.get("proveedor") == "fallback_local", "Self-test: proveedor esperado fallback_local"
    assert "texto_minimizado" in resultado and resultado["texto_minimizado"], "Self-test: texto minimizado vacío"
    assert evidencias["json"].exists(), "Self-test: no se generó JSON"
    assert evidencias["markdown"].exists(), "Self-test: no se generó Markdown"

    print("Self-test demo interactiva: OK")
    print(f"- Evidencia JSON: {evidencias['json']}")
    print(f"- Evidencia Markdown: {evidencias['markdown']}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Servidor local de demo interactiva de privacidad IA")
    parser.add_argument("--host", default=HOST)
    parser.add_argument("--port", type=int, default=PORT)
    parser.add_argument("--self-test", action="store_true", help="Ejecuta una prueba local sin levantar servidor")
    args = parser.parse_args()

    if args.self_test:
        ejecutar_self_test()
        return

    if args.host != HOST:
        raise ValueError("Por seguridad, el servidor solo puede ejecutarse en 127.0.0.1")

    server = HTTPServer((args.host, args.port), DemoHandler)
    print(f"Servidor demo interactiva disponible en http://{args.host}:{args.port}")
    print("Pulsa Ctrl+C para detener")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
