import json
from dataclasses import asdict

from app.config import RUTA_DATOS_BRUTOS, TOP_K_RECUPERACION
from componentes.segmentador import segmentar_documentos
from componentes.recuperador_hibrido import recuperar_hibrido
from componentes.reordenador_resultados import reordenar_resultados
from observabilidad.costes_simulados import estimar_coste_simulado
from observabilidad.trazas import crear_traza
from seguridad.filtro_salida import validar_salida_con_citas
from seguridad.guardia_entrada import validar_consulta
from servicios.generador_respuesta import generar_respuesta_extractiva


def _cargar_documentos() -> list[dict]:
    with RUTA_DATOS_BRUTOS.open("r", encoding="utf-8") as f:
        return json.load(f)


def ejecutar_pipeline(consulta: str) -> dict:
    traza = crear_traza("pipeline_rag")
    ok, motivo = validar_consulta(consulta)
    traza.registrar("validacion_entrada", {"ok": ok, "motivo": motivo})
    if not ok:
        return {
            "respuesta": f"Consulta bloqueada: {motivo}",
            "citas": [],
            "resultados": [],
            "trazas": traza.eventos,
            "coste_simulado": estimar_coste_simulado(consulta, 0),
        }

    documentos = _cargar_documentos()
    traza.registrar("carga_documentos", {"total": len(documentos)})
    fragmentos = segmentar_documentos(documentos)
    traza.registrar("segmentacion", {"fragmentos": len(fragmentos)})

    recuperados = recuperar_hibrido(consulta, fragmentos, top_k=TOP_K_RECUPERACION)
    traza.registrar("recuperacion", {"top_k": len(recuperados)})
    reordenados = reordenar_resultados(consulta, recuperados)
    traza.registrar("reordenacion", {"top": len(reordenados)})

    salida = generar_respuesta_extractiva(consulta, reordenados)
    ok_salida, motivo_salida = validar_salida_con_citas(salida)
    traza.registrar("filtro_salida", {"ok": ok_salida, "motivo": motivo_salida})
    if not ok_salida:
        salida = {
            "respuesta": "No puedo responder sin citas documentales válidas.",
            "citas": [],
        }

    coste = estimar_coste_simulado(consulta, len(reordenados))
    traza.registrar("coste", coste)

    resultados_dict = [
        {
            "fragmento": asdict(r.fragmento),
            "puntuacion": r.puntuacion,
            "detalle": r.detalle,
        }
        for r in reordenados
    ]
    return {
        "respuesta": salida["respuesta"],
        "citas": salida["citas"],
        "resultados": resultados_dict,
        "trazas": traza.eventos,
        "coste_simulado": coste,
    }
