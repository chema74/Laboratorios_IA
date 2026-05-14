import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from app.config import RUTA_PANEL
from servicios.motor_observabilidad import ejecutar_motor_observabilidad


def main() -> None:
    r = ejecutar_motor_observabilidad()
    html = f"""<!doctype html>
<html lang=\"es\"><head><meta charset=\"utf-8\"><title>Panel Observabilidad IA</title>
<style>body{{font-family:Arial,sans-serif;margin:24px}}.kpi{{padding:8px;border:1px solid #ccc;margin:6px 0}}</style></head>
<body>
<h1>Panel Observabilidad IA (Local)</h1>
<div class=\"kpi\">Eventos: {r['resumen_eventos']['total']}</div>
<div class=\"kpi\">Coste total simulado: {r['costes']['coste_total']} EUR</div>
<div class=\"kpi\">Latencia media: {r['latencias']['media']} ms | P95: {r['latencias']['p95_aprox']} ms</div>
<div class=\"kpi\">Tasa error: {r['errores']['tasa_error']}</div>
<div class=\"kpi\">Satisfacción media: {r['feedback']['satisfaccion_media']}</div>
<div class=\"kpi\">Estado presupuesto: {r['presupuesto']['estado']}</div>
<h2>Alertas</h2><ul>
{''.join([f"<li>{a['tipo']} ({a['severidad']}): {a['detalle']}</li>" for a in r['alertas_degradacion']]) or '<li>Sin alertas</li>'}
</ul>
</body></html>"""
    RUTA_PANEL.parent.mkdir(parents=True, exist_ok=True)
    RUTA_PANEL.write_text(html, encoding="utf-8")
    print(f"Panel generado en: {RUTA_PANEL}")


if __name__ == "__main__":
    main()
