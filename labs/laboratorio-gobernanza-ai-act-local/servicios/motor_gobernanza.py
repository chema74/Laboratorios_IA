import json

from app.config import RUTA_CASOS, RUTA_EVID, RUTA_OBLIG, RUTA_SHADOW
from gobernanza.alfabetizacion_ia import generar_plan_alfabetizacion
from gobernanza.clasificador_riesgo import clasificar_caso
from gobernanza.ficha_sistema_ia import generar_ficha_markdown
from gobernanza.inventario_casos_uso import cargar_casos, resumir_inventario
from gobernanza.matriz_obligaciones import obligaciones_por_riesgo
from gobernanza.politica_uso_responsable import generar_politica
from gobernanza.registro_evidencias import validar_evidencias
from gobernanza.shadow_ia import analizar_shadow_ia
from observabilidad.costes_simulados import coste_revision
from observabilidad.trazas import Traza


def _load(path):
    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def ejecutar_motor() -> dict:
    tr = Traza()
    casos = cargar_casos(RUTA_CASOS)
    evid = _load(RUTA_EVID)
    obligaciones = _load(RUTA_OBLIG)
    shadow = _load(RUTA_SHADOW)
    tr.registrar("carga_datos", {"casos": len(casos)})

    clasificados = []
    faltantes = []
    fichas = []
    for c in casos:
        cr = clasificar_caso(c)
        ob = obligaciones_por_riesgo(cr["categoria"], obligaciones)
        ev = validar_evidencias(c["identificador"], evid)
        clasificados.append({"caso": c, "clasificacion": cr, "obligaciones": ob, "evidencias": ev})
        if not ev["completo"]:
            faltantes.append(ev)
        fichas.append({"id": c["identificador"], "contenido": generar_ficha_markdown(c, cr, ev)})

    shadow_out = analizar_shadow_ia(shadow)
    resumen = resumir_inventario(casos)
    plan = generar_plan_alfabetizacion()
    politica = generar_politica()
    coste = coste_revision(len(casos))

    tr.registrar("analisis", {"clasificados": len(clasificados), "shadow_alertas": len(shadow_out)})
    return {
        "resumen_inventario": resumen,
        "casos_clasificados": clasificados,
        "evidencias_faltantes": faltantes,
        "shadow_ia": shadow_out,
        "plan_alfabetizacion": plan,
        "politica_uso_responsable": politica,
        "coste_simulado": coste,
        "fichas": fichas,
        "trazas": tr.eventos,
    }
