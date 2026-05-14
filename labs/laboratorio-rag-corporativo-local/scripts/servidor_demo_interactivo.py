import argparse
import json
import os
import sys
from datetime import datetime, timezone
from html import escape
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs

BASE = Path(__file__).resolve().parents[1]
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from app.config import RUTA_EVIDENCIAS_INTERACTIVAS
from servicios.analisis_llm import MODELO_POR_DEFECTO, analizar_rag_llm
from servicios.rag_llm import ejecutar_rag_con_llm

HOST = "127.0.0.1"
PORT = 8767

CONSULTAS_EJEMPLO = {
    "gastos": "Resume la política interna de gastos y aclara límites y aprobaciones.",
    "cumplimiento": "¿Qué riesgos aparecen en los documentos de cumplimiento corporativo?",
    "operaciones": "Extrae obligaciones y responsables para operaciones en este trimestre.",
    "direccion": "Prepara un informe ejecutivo para dirección con riesgos y recomendaciones.",
    "auditoria": "Resume evidencia documental útil para auditoría interna y trazabilidad.",
}

CAMPOS_TEXTO = ("texto", "contenido", "fragmento", "documento", "titulo", "referencia")


def _bool_form(valor: str | None) -> bool:
    if valor is None:
        return False
    return valor.strip().lower() in {"1", "true", "on", "yes", "si"}


def _texto_seguro(valor: object) -> str:
    if isinstance(valor, str):
        return valor
    try:
        return json.dumps(valor, ensure_ascii=False)
    except Exception:
        return str(valor)


def _texto_de_fragmento(fragmento: object) -> str:
    if isinstance(fragmento, str):
        return fragmento
    if isinstance(fragmento, dict):
        for campo in CAMPOS_TEXTO:
            candidato = fragmento.get(campo)
            if isinstance(candidato, str) and candidato.strip():
                return candidato.strip()
            if isinstance(candidato, (dict, list)):
                serializado = _texto_seguro(candidato).strip()
                if serializado:
                    return serializado
        return _texto_seguro(fragmento)
    return _texto_seguro(fragmento)


def _normalizar_fragmento(fragmento: object, indice: int) -> dict[str, str]:
    if isinstance(fragmento, dict):
        titulo = _texto_seguro(fragmento.get("titulo") or fragmento.get("documento") or fragmento.get("doc_id") or f"Fragmento {indice}")
        referencia = _texto_seguro(fragmento.get("referencia") or fragmento.get("doc_id") or "")
        score = fragmento.get("puntuacion")
        if score is None:
            score = fragmento.get("score")
        score_txt = _texto_seguro(score) if score is not None else ""
        texto = _texto_de_fragmento(fragmento)
        return {
            "titulo": titulo,
            "referencia": referencia,
            "score": score_txt,
            "posicion": str(indice),
            "texto": texto,
        }

    return {
        "titulo": f"Fragmento {indice}",
        "referencia": "",
        "score": "",
        "posicion": str(indice),
        "texto": _texto_de_fragmento(fragmento),
    }


def _fragmentos_normalizados(fragmentos: list[object]) -> list[dict[str, str]]:
    salida: list[dict[str, str]] = []
    for i, fragmento in enumerate(fragmentos, start=1):
        salida.append(_normalizar_fragmento(fragmento, i))
    return salida


def ejecutar_consulta_interactiva(
    consulta: str,
    usar_groq: bool,
    forzar_fallback_local: bool,
    api_key: str | None = None,
    opener=None,
) -> dict:
    q = (consulta or "").strip()
    if not q:
        raise ValueError("Debes indicar una consulta")

    rag = ejecutar_rag_con_llm(q)
    entorno = dict(os.environ)
    if forzar_fallback_local or not usar_groq:
        entorno["FORZAR_FALLBACK_LOCAL"] = "1"
    else:
        entorno.pop("FORZAR_FALLBACK_LOCAL", None)

    clave = api_key if api_key is not None else (entorno.get("GROQ_API_KEY") if usar_groq and not forzar_fallback_local else None)
    kwargs = {}
    if opener is not None:
        kwargs["opener"] = opener

    llm = analizar_rag_llm(
        q,
        rag["fragmentos"],
        api_key=clave,
        cargar_env=False,
        entorno=entorno,
        **kwargs,
    )

    return {
        "fecha": datetime.now(timezone.utc).isoformat(),
        "consulta": q,
        "rag": rag,
        "analisis_llm": llm,
        "proveedor": llm.get("proveedor", "desconocido"),
        "modelo": llm.get("modelo", llm.get("trazabilidad", {}).get("groq_model", "desconocido")),
        "ruta_ejecucion": llm.get("trazabilidad", {}).get("ruta_ejecucion", "indefinida"),
        "motivo_fallback": llm.get("motivo_fallback", ""),
    }


def _render_md(resultado: dict, json_path: Path) -> str:
    llm = resultado.get("analisis_llm", {})
    resp = llm.get("respuesta", {})
    lineas = [
        "# Evidencia interactiva RAG V2.1",
        "",
        f"- Fecha UTC: {resultado.get('fecha', 'n/a')}",
        f"- Consulta: {resultado.get('consulta', '')}",
        f"- Proveedor: {resultado.get('proveedor', 'desconocido')}",
        f"- Modelo: {resultado.get('modelo', 'desconocido')}",
        f"- Ruta ejecución: {resultado.get('ruta_ejecucion', 'indefinida')}",
        f"- JSON asociado: {json_path}",
    ]
    if resultado.get("motivo_fallback"):
        lineas.append(f"- Motivo fallback: {resultado['motivo_fallback']}")

    lineas.extend(["", "## Fragmentos recuperados"])
    for fr in _fragmentos_normalizados(resultado.get("rag", {}).get("fragmentos", [])[:6]):
        lineas.append(
            f"- [{fr['posicion']}] {fr['titulo']} | Ref: {fr['referencia'] or 'n/a'} | Score: {fr['score'] or 'n/a'} | {fr['texto'][:220]}"
        )

    lineas.extend(["", "## Respuesta"])
    lineas.append(_texto_seguro(resp.get("resumen", "Sin resumen")))

    lineas.extend(["", "## Riesgos"])
    for r in resp.get("riesgos", []):
        lineas.append(f"- {_texto_seguro(r)}")

    lineas.extend(["", "## Recomendaciones"])
    for rec in resp.get("recomendaciones", []):
        lineas.append(f"- {_texto_seguro(rec)}")

    lineas.extend([
        "",
        "## Licencia y Autoría",
        "Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.",
        "",
        "© 2026 – Txema Ríos.",
    ])
    return "\n".join(lineas)


def guardar_evidencia_interactiva(resultado: dict, carpeta: Path | None = None) -> dict:
    destino = carpeta or RUTA_EVIDENCIAS_INTERACTIVAS
    destino.mkdir(parents=True, exist_ok=True)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    ruta_json = destino / f"{ts}_resultado.json"
    ruta_md = destino / f"{ts}_informe.md"

    llm = resultado.get("analisis_llm", {})
    resp = llm.get("respuesta", {})
    payload = {
        "fecha": resultado.get("fecha"),
        "consulta": resultado.get("consulta"),
        "fragmentos_recuperados": resultado.get("rag", {}).get("fragmentos", []),
        "respuesta": resp,
        "proveedor": resultado.get("proveedor"),
        "modelo": resultado.get("modelo"),
        "ruta_ejecucion": resultado.get("ruta_ejecucion"),
        "motivo_fallback": resultado.get("motivo_fallback", ""),
    }
    ruta_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    ruta_md.write_text(_render_md(resultado, ruta_json), encoding="utf-8")
    return {"json": ruta_json, "markdown": ruta_md}


def _opciones_html() -> str:
    partes = ["<option value=''>-- Selecciona escenario --</option>"]
    for k, v in CONSULTAS_EJEMPLO.items():
        partes.append(f"<option value=\"{escape(k)}\">{escape(v)}</option>")
    return "\n".join(partes)


def _badge(texto: str, clase: str = "") -> str:
    clase_extra = f" {clase}" if clase else ""
    return f"<span class=\"badge{clase_extra}\">{escape(texto)}</span>"


def _render_estado(resultado: dict | None) -> str:
    if not resultado:
        return ""
    proveedor = _texto_seguro(resultado.get("proveedor", "desconocido"))
    clase = "ok" if proveedor == "groq" else "warn"
    modelo = _texto_seguro(resultado.get("modelo", "desconocido"))
    ruta = _texto_seguro(resultado.get("ruta_ejecucion", "indefinida"))
    return (
        "<div class=\"estado-ejecucion\">"
        f"{_badge(f'Proveedor: {proveedor}', clase)}"
        f"{_badge(f'Modelo: {modelo}')}"
        f"{_badge(f'Ruta: {ruta}')}"
        "</div>"
    )


def _render_fragmentos_cards(fragmentos: list[object]) -> str:
    bloques = []
    for fr in _fragmentos_normalizados(fragmentos):
        bloques.append(
            "<article class=\"fragmento-card\">"
            f"<header><strong>{escape(fr['titulo'])}</strong></header>"
            "<p class=\"meta\">"
            f"Posición: {escape(fr['posicion'])}"
            f" · Referencia: {escape(fr['referencia'] or 'n/a')}"
            f" · Score: {escape(fr['score'] or 'n/a')}"
            "</p>"
            f"<p>{escape(fr['texto'])}</p>"
            "</article>"
        )
    if not bloques:
        return "<p>Sin fragmentos recuperados.</p>"
    return "".join(bloques)


def _render_page(resultado: dict | None = None, error: str = "") -> str:
    bloque_resultado = """
        <section class="card" id="bloque-resultado">
          <h2>Resultado de la ejecución</h2>
          <p class="small">Todavía no se ha ejecutado ninguna consulta en esta vista.</p>
          <h3>Fragmentos recuperados</h3>
          <p>Sin fragmentos recuperados.</p>
          <h3>Evidencias generadas</h3>
          <ul id="bloque-evidencias">
            <li><strong>Markdown:</strong> <code id="ruta-md">n/a</code></li>
            <li><strong>JSON:</strong> <code id="ruta-json">n/a</code></li>
          </ul>
        </section>
    """
    if resultado:
        llm = resultado.get("analisis_llm", {})
        resp = llm.get("respuesta", {})
        motivo = _texto_seguro(resultado.get("motivo_fallback", ""))
        motivo_html = f"<p><strong>Motivo fallback:</strong> {escape(motivo)}</p>" if motivo else ""
        ev = resultado.get("evidencias", {})
        riesgos = "".join(f"<li>{escape(_texto_seguro(x))}</li>" for x in resp.get("riesgos", [])) or "<li>Sin riesgos</li>"
        recs = "".join(f"<li>{escape(_texto_seguro(x))}</li>" for x in resp.get("recomendaciones", [])) or "<li>Sin recomendaciones</li>"
        frag_cards = _render_fragmentos_cards(resultado.get("rag", {}).get("fragmentos", []))

        bloque_resultado = f"""
        <section class=\"card\" id=\"bloque-resultado\">
          <h2>Resultado de la ejecución</h2>
          {_render_estado(resultado)}
          <div class=\"two-cols\">
            <div>
              <h3>Consulta ejecutada</h3>
              <p id=\"consulta-ejecutada\">{escape(_texto_seguro(resultado.get('consulta', '')))}</p>
              <h3>Respuesta generada</h3>
              <p id=\"respuesta-generada\">{escape(_texto_seguro(resp.get('resumen', 'Sin resumen')))}</p>
              <h3>Trazabilidad</h3>
              <p><strong>Fecha/hora:</strong> {escape(_texto_seguro(resultado.get('fecha', 'n/a')))}</p>
              <p><strong>Proveedor:</strong> {escape(_texto_seguro(resultado.get('proveedor', 'desconocido')))}</p>
              <p><strong>Modelo:</strong> {escape(_texto_seguro(resultado.get('modelo', 'desconocido')))}</p>
              <p><strong>Ruta de ejecución:</strong> {escape(_texto_seguro(resultado.get('ruta_ejecucion', 'indefinida')))}</p>
              {motivo_html}
            </div>
            <div>
              <h3>Riesgos</h3>
              <ul>{riesgos}</ul>
              <h3>Recomendaciones</h3>
              <ul>{recs}</ul>
            </div>
          </div>

          <h3>Fragmentos recuperados</h3>
          <div id=\"fragmentos-recuperados\" class=\"grid-fragmentos\">{frag_cards}</div>

          <h3>Evidencias generadas</h3>
          <ul id=\"bloque-evidencias\">
            <li><strong>Markdown:</strong> <code id=\"ruta-md\">{escape(_texto_seguro(ev.get('markdown', 'n/a')))}</code></li>
            <li><strong>JSON:</strong> <code id=\"ruta-json\">{escape(_texto_seguro(ev.get('json', 'n/a')))}</code></li>
          </ul>

          <div class=\"acciones\">
            <button type=\"button\" data-copy-target=\"respuesta-generada\">Copiar respuesta</button>
            <button type=\"button\" data-copy-target=\"consulta-ejecutada\">Copiar consulta</button>
            <button type=\"button\" data-copy-target=\"fragmentos-recuperados\">Copiar fragmentos</button>
            <button type=\"button\" data-copy-target=\"ruta-md\">Abrir evidencia Markdown</button>
            <button type=\"button\" data-copy-target=\"ruta-json\">Abrir evidencia JSON</button>
          </div>
        </section>
        """

    error_html = f"<p class='error'>No se pudo procesar la consulta: {escape(error)}</p>" if error else ""
    groq_disponible = "Sí" if os.getenv("GROQ_API_KEY") else "No"
    modelo_cfg = str(os.getenv("GROQ_MODEL", MODELO_POR_DEFECTO)).strip() or MODELO_POR_DEFECTO

    return f"""<!doctype html>
<html lang=\"es\"><head>
<meta charset=\"utf-8\" />
<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
<title>Laboratorio RAG corporativo local — Demo interactiva V2.1</title>
<style>
:root{{
  --bg:#f4f7fb;
  --card:#ffffff;
  --ink:#13263a;
  --muted:#5d738a;
  --line:#d6e1ef;
  --brand:#0d5f98;
  --brand2:#0a8b83;
  --ok:#0a7f5a;
  --warn:#9a5a08;
  --error:#9f2d1b;
}}
*{{box-sizing:border-box}}
body{{margin:0;background:linear-gradient(180deg,#eff5fc 0%,#f7fbff 40%,#eef7f6 100%);color:var(--ink);font-family:Segoe UI,Tahoma,sans-serif}}
.wrap{{max-width:1180px;margin:20px auto;padding:0 16px 32px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px;margin-bottom:14px;box-shadow:0 6px 18px rgba(19,38,58,.06)}}
.header-title{{margin:0 0 6px;font-size:1.5rem}}
.header-sub{{margin:0 0 10px;color:var(--muted)}}
.badge{{display:inline-block;margin-right:8px;margin-bottom:6px;padding:5px 10px;border-radius:999px;background:#e8f2fb;border:1px solid #bfd8ef;font-size:.86rem}}
.badge.ok{{background:#e5f7ef;border-color:#b8e8d3;color:var(--ok)}}
.badge.warn{{background:#fff2de;border-color:#f3d6a7;color:var(--warn)}}
label{{display:block;font-weight:700;margin-top:10px}}
textarea,select{{width:100%;padding:10px;border:1px solid #c8d7e8;border-radius:8px;font-family:inherit;background:#fff}}
textarea{{min-height:120px}}
.small{{color:var(--muted);font-size:.92rem;margin:6px 0}}
.mode-box{{padding:10px;border-radius:10px;border:1px dashed #b6cee5;background:#f5faff;margin-top:10px}}
.actions-top,.acciones{{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}}
button{{background:var(--brand);color:#fff;border:none;border-radius:8px;padding:10px 13px;font-weight:700;cursor:pointer}}
button.alt{{background:#35526f}}
button.soft{{background:#eef3f8;color:#153047;border:1px solid #c5d4e6}}
button:hover{{filter:brightness(.97)}}
.error{{color:var(--error);font-weight:700}}
.two-cols{{display:grid;grid-template-columns:1fr;gap:14px}}
.estado-ejecucion{{margin-bottom:10px}}
.grid-fragmentos{{display:grid;grid-template-columns:1fr;gap:10px}}
.fragmento-card{{border:1px solid #d8e5f3;border-radius:10px;padding:12px;background:#fbfdff}}
.fragmento-card .meta{{color:var(--muted);font-size:.9rem;margin:8px 0}}
.status-bar{{margin-top:8px;padding:10px;border-radius:10px;border:1px solid #d7e5f2;background:#f7fbff;color:#1a4465;font-weight:600}}
.historial button{{background:#f0f6fd;color:#10314c;border:1px solid #c5d8ec}}
code{{word-break:break-all}}
@media (min-width:900px){{
  .two-cols{{grid-template-columns:1.25fr 1fr}}
  .grid-fragmentos{{grid-template-columns:1fr 1fr}}
}}
</style>
</head><body><div class=\"wrap\">
<section class=\"card\" id=\"cabecera-demo\">
  <h1 class=\"header-title\">Laboratorio RAG corporativo local — Demo interactiva V2.1</h1>
  <p class=\"header-sub\">Consulta documentos corporativos, recupera fragmentos y genera respuestas con Groq opcional o fallback local.</p>
  {_badge(f"GROQ_API_KEY detectada: {groq_disponible}", 'ok' if groq_disponible == 'Sí' else 'warn')}
  {_badge(f"Modelo configurado: {modelo_cfg}")}
  {error_html}
</section>

<section class=\"card\" id=\"panel-consulta\">
  <h2>Consulta y modo de ejecución</h2>
  <form method=\"post\" action=\"/consultar\" id=\"form-consulta\">
    <label for=\"ejemplo\">Escenarios predefinidos</label>
    <select id=\"ejemplo\" name=\"ejemplo\">{_opciones_html()}</select>

    <label for=\"consulta\">Consulta editable</label>
    <textarea id=\"consulta\" name=\"consulta\" placeholder=\"Escribe una consulta corporativa...\"></textarea>

    <div class=\"actions-top\">
      <button type=\"button\" class=\"soft\" id=\"btn-cargar\">Cargar consulta de ejemplo</button>
      <button type=\"button\" class=\"soft\" id=\"btn-limpiar\">Limpiar consulta</button>
    </div>

    <div class=\"mode-box\" id=\"bloque-trazabilidad\">
      <p class=\"small\"><strong>Modo de ejecución:</strong> configura cómo se genera la respuesta.</p>
      <p><label><input type=\"checkbox\" name=\"usar_groq\" value=\"1\" checked/> Usar Groq si hay GROQ_API_KEY</label></p>
      <p class=\"small\">Usa LLM remoto para respuesta enriquecida cuando haya clave disponible.</p>
      <p><label><input type=\"checkbox\" name=\"forzar_fallback\" value=\"1\"/> Forzar fallback local</label></p>
      <p class=\"small\">Ejecuta modo determinista local sin depender de Groq.</p>
    </div>

    <div class=\"actions-top\">
      <button type=\"submit\" id=\"btn-ejecutar\">Ejecutar consulta</button>
    </div>
    <div class=\"status-bar\" id=\"estado-ui\">Estado: lista para ejecutar.</div>
  </form>
</section>

<section class=\"card\" id=\"bloque-historial\">
  <h2>Historial local de consultas</h2>
  <p class=\"small\">Se guarda en la sesión actual del navegador. Haz clic para reutilizar una consulta.</p>
  <div class=\"historial\" id=\"historial-consultas\"></div>
</section>

<section class=\"card\" id=\"bloque-que-demuestra\">
  <h2>Qué demuestra esta demo</h2>
  <ul>
    <li>Recuperación de información corporativa relevante por consulta.</li>
    <li>Grounding en fragmentos recuperados para responder con evidencia.</li>
    <li>Respuesta con LLM opcional mediante Groq cuando está disponible.</li>
    <li>Fallback local determinista para continuidad sin red o sin clave.</li>
    <li>Evidencia reproducible por ejecución en JSON y Markdown.</li>
  </ul>
</section>

{bloque_resultado}

<script>
(function() {{
  const escenarios = {json.dumps(CONSULTAS_EJEMPLO, ensure_ascii=False)};
  const sel = document.getElementById('ejemplo');
  const txt = document.getElementById('consulta');
  const estado = document.getElementById('estado-ui');
  const historialBox = document.getElementById('historial-consultas');
  const KEY = 'demo_rag_historial_v21';

  function cargarHistorial() {{
    try {{
      return JSON.parse(sessionStorage.getItem(KEY) || '[]');
    }} catch (_e) {{
      return [];
    }}
  }}

  function guardarHistorial(items) {{
    sessionStorage.setItem(KEY, JSON.stringify(items.slice(0, 8)));
  }}

  function renderHistorial() {{
    const items = cargarHistorial();
    if (!items.length) {{
      historialBox.innerHTML = '<p class="small">Todavía no hay consultas en esta sesión.</p>';
      return;
    }}
    historialBox.innerHTML = items.map((q, i) =>
      `<button type="button" data-q="${{q.replace(/"/g, '&quot;')}}">${{i + 1}}. ${{q}}</button>`
    ).join(' ');
    historialBox.querySelectorAll('button').forEach((b) => {{
      b.addEventListener('click', () => {{
        txt.value = b.getAttribute('data-q') || '';
        estado.textContent = 'Estado: consulta recuperada desde historial local.';
      }});
    }});
  }}

  function registrarConsulta(q) {{
    const limpia = (q || '').trim();
    if (!limpia) return;
    const hist = [limpia, ...cargarHistorial().filter((x) => x !== limpia)];
    guardarHistorial(hist);
    renderHistorial();
  }}

  document.getElementById('btn-cargar').addEventListener('click', () => {{
    const clave = sel.value;
    txt.value = escenarios[clave] || '';
    estado.textContent = 'Estado: consulta de ejemplo cargada.';
  }});

  document.getElementById('btn-limpiar').addEventListener('click', () => {{
    txt.value = '';
    estado.textContent = 'Estado: consulta limpiada.';
  }});

  sel.addEventListener('change', () => {{
    txt.value = escenarios[sel.value] || '';
    if (txt.value) estado.textContent = 'Estado: escenario seleccionado y consulta propuesta cargada.';
  }});

  document.getElementById('form-consulta').addEventListener('submit', () => {{
    const q = txt.value.trim() || escenarios[sel.value] || '';
    registrarConsulta(q);
    estado.textContent = 'Preparando consulta…';
    setTimeout(() => {{ estado.textContent = 'Recuperando fragmentos…'; }}, 220);
    setTimeout(() => {{ estado.textContent = 'Generando respuesta…'; }}, 520);
    setTimeout(() => {{ estado.textContent = 'Evidencia guardada…'; }}, 900);
  }});

  document.querySelectorAll('[data-copy-target]').forEach((btn) => {{
    btn.addEventListener('click', async () => {{
      const id = btn.getAttribute('data-copy-target');
      const el = document.getElementById(id);
      const texto = (el && (el.innerText || el.textContent) || '').trim();
      if (!texto) return;
      try {{
        await navigator.clipboard.writeText(texto);
        estado.textContent = 'Estado: contenido copiado al portapapeles.';
      }} catch (_e) {{
        estado.textContent = 'Estado: no se pudo copiar automáticamente; revisa permisos del navegador.';
      }}
    }});
  }});

  renderHistorial();
}})();
</script>
</div></body></html>"""


class Handler(BaseHTTPRequestHandler):
    def _responder(self, html: str, status: int = 200) -> None:
        data = html.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:
        if self.path in {"/", "/index.html"}:
            self._responder(_render_page())
            return
        self._responder(_render_page(error="Ruta no encontrada"), status=404)

    def do_POST(self) -> None:
        if self.path != "/consultar":
            self._responder(_render_page(error="Ruta POST no válida"), status=404)
            return

        longitud = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(longitud).decode("utf-8")
        form = parse_qs(body)

        ejemplo = (form.get("ejemplo", [""])[0] or "").strip()
        consulta = (form.get("consulta", [""])[0] or "").strip()
        usar_groq = _bool_form(form.get("usar_groq", [None])[0])
        forzar_fallback = _bool_form(form.get("forzar_fallback", [None])[0])

        q = consulta or CONSULTAS_EJEMPLO.get(ejemplo, "")
        try:
            resultado = ejecutar_consulta_interactiva(q, usar_groq=usar_groq, forzar_fallback_local=forzar_fallback)
            ev = guardar_evidencia_interactiva(resultado)
            resultado["evidencias"] = {"json": str(ev["json"]), "markdown": str(ev["markdown"])}
            self._responder(_render_page(resultado=resultado))
        except Exception:
            self._responder(
                _render_page(error="revisa la consulta o el modo de ejecución configurado"),
                status=400,
            )


def ejecutar_self_test() -> None:
    resultado = ejecutar_consulta_interactiva(
        CONSULTAS_EJEMPLO["cumplimiento"],
        usar_groq=False,
        forzar_fallback_local=True,
    )
    evidencias = guardar_evidencia_interactiva(resultado)

    assert resultado.get("proveedor") == "fallback_local"
    assert resultado.get("rag", {}).get("fragmentos") is not None
    assert evidencias["json"].exists()
    assert evidencias["markdown"].exists()

    print("Self-test demo interactiva RAG: OK")
    print(f"- Evidencia JSON: {evidencias['json']}")
    print(f"- Evidencia Markdown: {evidencias['markdown']}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Servidor local de demo interactiva RAG")
    parser.add_argument("--host", default=HOST)
    parser.add_argument("--port", type=int, default=PORT)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        ejecutar_self_test()
        return

    if args.host != HOST:
        raise ValueError("Por seguridad, el servidor solo puede ejecutarse en 127.0.0.1")

    servidor = HTTPServer((args.host, args.port), Handler)
    print(f"Servidor demo interactiva disponible en http://{args.host}:{args.port}")
    print("Pulsa Ctrl+C para detener")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        servidor.server_close()


if __name__ == "__main__":
    main()
