from __future__ import annotations

import argparse
import html
import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs

BASE = Path(__file__).resolve().parents[1]
SRC = BASE / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from observabilidad_costes_ia.escenarios import ESCENARIOS_PREDEFINIDOS, obtener_escenario
from observabilidad_costes_ia.motor import analizar_eventos
from observabilidad_costes_ia.orquestador import generar_analisis_ejecutivo


def construir_contexto(nombre_escenario: str, eventos_texto: str | None = None) -> dict[str, object]:
    eventos = obtener_escenario(nombre_escenario)
    error_parseo = ""

    if eventos_texto:
        try:
            eventos = json.loads(eventos_texto)
            if not isinstance(eventos, list):
                raise ValueError("El JSON debe ser una lista de eventos.")
        except (json.JSONDecodeError, ValueError) as exc:
            error_parseo = f"Entrada personalizada invalida: {exc}"

    metrica = analizar_eventos(eventos)
    analisis = generar_analisis_ejecutivo(metrica)

    return {
        "escenario": nombre_escenario,
        "eventos": metrica["eventos"],
        "metrica": metrica,
        "analisis": analisis,
        "error_parseo": error_parseo,
        "json_eventos": json.dumps(eventos, ensure_ascii=False, indent=2),
    }


def render_html(contexto: dict[str, object]) -> str:
    metrica = contexto["metrica"]
    analisis = contexto["analisis"]
    filas = "".join(
        "<tr>"
        f"<td>{html.escape(str(ev['id_evento']))}</td>"
        f"<td>{html.escape(str(ev['caso_uso']))}</td>"
        f"<td>{html.escape(str(ev['modelo']))}</td>"
        f"<td>{html.escape(str(ev['proveedor']))}</td>"
        f"<td>{ev['tokens_entrada'] + ev['tokens_salida']}</td>"
        f"<td>{ev['latencia_ms']}</td>"
        f"<td>{ev['coste_estimado_eur']:.4f}</td>"
        f"<td>{html.escape(str(ev['estado']))}</td>"
        f"<td>{html.escape(str(ev['riesgo']))}</td>"
        "</tr>"
        for ev in metrica["eventos"]
    )

    opciones = "".join(
        f"<option value=\"{k}\" {'selected' if k == contexto['escenario'] else ''}>{k}</option>"
        for k in ESCENARIOS_PREDEFINIDOS
    )

    alertas = "".join(
        f"<li><strong>{html.escape(a['tipo'])}</strong>: {html.escape(a['detalle'])}</li>" for a in metrica["alertas"]
    ) or "<li>Sin alertas activas.</li>"

    recomendaciones = "".join(f"<li>{html.escape(str(r))}</li>" for r in metrica["recomendaciones_operativas"])
    riesgos = "".join(f"<li>{html.escape(str(r))}</li>" for r in analisis.get("riesgos_detectados", []))

    diagnostico_groq = analisis.get("diagnostico_groq")
    diagnostico_html = ""
    if isinstance(diagnostico_groq, dict):
        diagnostico_html = (
            "<p><strong>Diagnóstico Groq:</strong> "
            f"estado={html.escape(str(diagnostico_groq.get('estado')))}, "
            f"categoria={html.escape(str(diagnostico_groq.get('categoria', '-')))}, "
            f"http_status={html.escape(str(diagnostico_groq.get('http_status', '-')))}</p>"
        )

    return f"""<!doctype html>
<html lang=\"es\"><head><meta charset=\"utf-8\"><title>Dashboard V2.1 Observabilidad y Costes IA</title>
<style>
:root{{--fondo:#f4f7fb;--texto:#0f172a;--tarjeta:#ffffff;--acento:#0ea5e9;--ok:#14532d;--warn:#b45309;}}
body{{font-family:Segoe UI,Arial,sans-serif;background:linear-gradient(120deg,#e0f2fe,#f8fafc);color:var(--texto);margin:0;padding:20px}}
main{{max-width:1100px;margin:auto}} .grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px}}
.card{{background:var(--tarjeta);padding:12px;border-radius:10px;border:1px solid #dbeafe}} table{{width:100%;border-collapse:collapse;background:white}}
th,td{{border:1px solid #d1d5db;padding:6px;font-size:12px;text-align:left}} textarea{{width:100%;min-height:150px}}
</style></head>
<body><main>
<h1>Laboratorio V2.1: Observabilidad y Costes de IA</h1>
<p>Demo empresarial local en menos de 60 segundos: métricas, alertas, recomendaciones y análisis ejecutivo con Groq opcional.</p>
<p><strong>Qué demuestra técnicamente:</strong> métricas agregadas, alertas por umbral, trazabilidad por evento, fallback determinista y capa LLM opcional.</p>
<p><strong>Cómo lo usaría una empresa:</strong> seguimiento diario de coste, latencia, errores y riesgos de gobernanza por caso de uso y equipo.</p>
<form method=\"post\">
<div class=\"card\"><label>Escenario predefinido:</label><select name=\"escenario\">{opciones}</select></div>
<div class=\"card\"><label>Pegar eventos JSON (opcional):</label><textarea name=\"eventos_json\">{html.escape(str(contexto['json_eventos']))}</textarea></div>
<button type=\"submit\">Analizar</button></form>
<p><strong>Modo análisis:</strong> {html.escape(str(analisis.get('modo', 'fallback_local')))} | <strong>Evidencias:</strong> evidencias/v2_1/</p>
{diagnostico_html}
<p style=\"color:#b91c1c\">{html.escape(str(contexto['error_parseo']))}</p>
<div class=\"grid">
<div class=\"card\"><strong>Total eventos</strong><br>{metrica['total_eventos']}</div>
<div class=\"card\"><strong>Coste total estimado</strong><br>{metrica['coste_total_estimado']:.4f} EUR</div>
<div class=\"card\"><strong>Tokens totales</strong><br>{metrica['tokens_totales']}</div>
<div class=\"card\"><strong>Latencia media</strong><br>{metrica['latencia_media_ms']} ms</div>
<div class=\"card\"><strong>Tasa de errores</strong><br>{metrica['tasa_errores']:.2%}</div>
<div class=\"card\"><strong>Eventos de riesgo</strong><br>{metrica['eventos_riesgo']}</div>
</div>
<h2>Alertas</h2><ul>{alertas}</ul>
<h2>Recomendaciones operativas</h2><ul>{recomendaciones}</ul>
<h2>Análisis ejecutivo</h2>
<p>{html.escape(str(analisis.get('resumen_ejecutivo', 'Sin resumen')))}</p>
<h3>Riesgos detectados</h3><ul>{riesgos}</ul>
<h2>Eventos analizados</h2>
<table><thead><tr><th>ID</th><th>Caso</th><th>Modelo</th><th>Proveedor</th><th>Tokens</th><th>Latencia</th><th>Coste EUR</th><th>Estado</th><th>Riesgo</th></tr></thead><tbody>{filas}</tbody></table>
</main></body></html>"""


class DashboardHandler(BaseHTTPRequestHandler):
    contexto = construir_contexto("uso_normal_controlado")

    def _responder(self):
        contenido = render_html(self.contexto).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(contenido)))
        self.end_headers()
        self.wfile.write(contenido)

    def do_GET(self):
        self._responder()

    def do_POST(self):
        longitud = int(self.headers.get("Content-Length", "0"))
        datos = self.rfile.read(longitud).decode("utf-8")
        form = parse_qs(datos)
        escenario = form.get("escenario", ["uso_normal_controlado"])[0]
        eventos_json = form.get("eventos_json", [""])[0]
        if escenario not in ESCENARIOS_PREDEFINIDOS:
            escenario = "uso_normal_controlado"
        self.contexto = construir_contexto(escenario, eventos_json)
        self._responder()


def main() -> None:
    parser = argparse.ArgumentParser(description="Dashboard local V2.1 de observabilidad y costes IA.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--puerto", default=8765, type=int)
    args = parser.parse_args()

    servidor = HTTPServer((args.host, args.puerto), DashboardHandler)
    print(f"Dashboard activo en: http://{args.host}:{args.puerto}")
    print("Pulsa Ctrl+C para detener.")
    servidor.serve_forever()


if __name__ == "__main__":
    main()
