"""Constructor principal de la demo narrativa integrada."""

from __future__ import annotations

import random
from datetime import date
from pathlib import Path

from .generador_indice_evidencias import construir_mapa_evidencias
from .linea_tiempo import construir_linea_tiempo
from .modelos import EpisodioNarrativo, FichaNarrativaEmpresa, dataclass_a_dict

ACCIONES_SIMULADAS = [
    "registrar_evento_y_documentar",
    "solicitar_revision_humana",
    "escalar_a_responsable_operaciones",
    "priorizar_riesgo_privacidad",
    "comparar_flujos_y_justificar",
]

RESULTADOS_SIMULADOS = [
    "resultado_sintetico_controlado",
    "resultado_sintetico_con_riesgo_moderado",
    "resultado_sintetico_escalado",
]


def _extraer_empresa(contexto: dict) -> tuple[str, str, str]:
    empresa = contexto.get("empresa", {})
    if isinstance(empresa, dict) and isinstance(empresa.get("empresa"), dict):
        base = empresa["empresa"]
    else:
        base = empresa if isinstance(empresa, dict) else {}
    return (
        str(base.get("id_empresa", "EMP-SINT-0001")),
        str(base.get("nombre", "Empresa Sintetica de Referencia")),
        str(base.get("sector", "servicios")),
    )


def _ids(lista: object, campo: str, maximo: int = 3) -> list[str]:
    if not isinstance(lista, list):
        return []
    out: list[str] = []
    for item in lista:
        if not isinstance(item, dict):
            continue
        valor = item.get(campo)
        if isinstance(valor, str) and valor:
            out.append(valor)
        if len(out) >= maximo:
            break
    return out


def _resumen_ejecutivo(
    nombre_empresa: str,
    dias: int,
    contexto: dict,
) -> dict:
    return {
        "empresa_simulada": nombre_empresa,
        "semana_simulada": f"{dias} dias operativos sinteticos",
        "eventos_destacados": _ids(contexto.get("eventos"), "id_evento", maximo=5),
        "crisis_destacadas": _ids(contexto.get("crisis"), "id_crisis", maximo=5),
        "alertas_principales": _ids(contexto.get("alertas"), "id_alerta", maximo=5),
        "riesgos_privacidad": _ids(contexto.get("riesgos_privacidad"), "id_riesgo", maximo=5),
        "revisiones_humanas": _ids(contexto.get("revisiones"), "id_revision", maximo=5),
        "comparativas_relevantes": _ids(contexto.get("comparaciones"), "id_comparacion", maximo=5),
        "valor_tecnico_del_laboratorio": (
            "Integra artefactos sintéticos de proyectos 01 a 10 para explicar "
            "trazabilidad, evaluación y control operativo en entorno local."
        ),
        "limites_explicitos": (
            "No representa actividad real de cliente, no ejecuta agentes reales, "
            "no usa APIs externas y no debe usarse como sistema productivo."
        ),
    }


def _resumen_demo(
    ficha: dict,
    hitos: list[dict],
    episodios: list[dict],
    evidencias: list[dict],
    contexto: dict,
    entradas_utilizadas: dict[str, str],
) -> dict:
    return {
        "fecha_generacion": ficha["fecha_generacion"],
        "empresa": ficha["nombre_empresa"],
        "total_dias_simulados": len(hitos),
        "total_hitos": len(hitos),
        "total_episodios": len(episodios),
        "evidencias_detectadas": len(evidencias),
        "proyectos_integrados": sorted({ev["proyecto_origen"] for ev in evidencias}),
        "crisis_incluidas": len(_ids(contexto.get("crisis"), "id_crisis", maximo=999)),
        "revisiones_humanas_incluidas": len(_ids(contexto.get("revisiones"), "id_revision", maximo=999)),
        "riesgos_privacidad_incluidos": len(_ids(contexto.get("riesgos_privacidad"), "id_riesgo", maximo=999)),
        "comparativas_incluidas": len(_ids(contexto.get("comparaciones"), "id_comparacion", maximo=999)),
        "entradas_utilizadas": entradas_utilizadas,
        "advertencia_sobre_datos_sinteticos": "Todos los artefactos usados en la demo son sintéticos.",
        "advertencia_sobre_no_sistema_productivo": "La demo no es un sistema productivo ni de monitorización real.",
        "advertencia_sobre_no_ejecucion_de_agentes": "No se ejecutan agentes reales ni modelos IA reales.",
    }


def construir_demo_narrativa(
    contexto: dict,
    seed: int,
    dias: int,
    base_repo: Path,
    entradas_utilizadas: dict[str, str],
) -> dict:
    rng = random.Random(seed)
    id_empresa, nombre_empresa, sector = _extraer_empresa(contexto)
    fecha_generacion = date.today().isoformat()
    fecha_inicio = date.today()

    ficha = FichaNarrativaEmpresa(
        id_demo=f"DEM-{seed:06d}",
        nombre_empresa=nombre_empresa,
        sector=sector,
        periodo_simulado=f"{dias} dias",
        fecha_generacion=fecha_generacion,
        origen_simulado=f"Proyecto 10 integrado sobre {id_empresa}",
        advertencia_sobre_datos_sinteticos=(
            "Demo narrativa basada exclusivamente en datos sintéticos del laboratorio."
        ),
    )
    ficha_dict = dataclass_a_dict(ficha)

    artefactos_hito = {
        "estado_inicial": ["estado_operativo.json"],
        "evento_negocio": ["eventos_negocio.json"],
        "documentacion": ["indice_documentos.json"],
        "escenario_prueba": ["escenarios_prueba_agentes.json"],
        "crisis_simulada": ["crisis_simuladas.json", "resumen_crisis.json"],
        "revision_humana": ["revisiones_humanas.json", "registro_decisiones.json"],
        "cierre_semanal": ["comparaciones_agente_proceso.json", "resumen_comparador.json"],
    }

    # 1) Construimos la línea temporal semanal para dar estructura narrativa.
    # 2) Generamos episodios por día enlazando eventos, crisis, privacidad y comparativas.
    # 3) Calculamos resumen y evidencias para una demo técnica trazable de portfolio.
    hitos = construir_linea_tiempo(seed=seed, dias=dias, fecha_inicio=fecha_inicio, nombre_empresa=nombre_empresa, artefactos=artefactos_hito)

    eventos_ids = _ids(contexto.get("eventos"), "id_evento", maximo=10)
    documentos_ids = _ids(contexto.get("documentos"), "id_documento", maximo=10)
    crisis_ids = _ids(contexto.get("crisis"), "id_crisis", maximo=10)
    revisiones_ids = _ids(contexto.get("revisiones"), "id_revision", maximo=10)
    riesgos_ids = _ids(contexto.get("riesgos_privacidad"), "id_riesgo", maximo=10)
    comparaciones_ids = _ids(contexto.get("comparaciones"), "id_comparacion", maximo=10)

    episodios: list[dict] = []
    for i, hito in enumerate(hitos, start=1):
        episodio = EpisodioNarrativo(
            id_episodio=f"EPI-{i:04d}",
            dia=hito["dia"],
            titulo=f"Episodio {i}: {hito['titulo']}",
            contexto=(
                "Escenario sintético de operación empresarial para evaluación técnica. "
                "No representa una operación real de cliente."
            ),
            problema_detectado=hito["descripcion"],
            datos_usados=["empresa_sintetica", "eventos_sinteticos", "documentos_sinteticos"],
            documentos_relacionados=documentos_ids[(i - 1) % len(documentos_ids): (i - 1) % len(documentos_ids) + 2] if documentos_ids else [],
            eventos_relacionados=eventos_ids[(i - 1) % len(eventos_ids): (i - 1) % len(eventos_ids) + 2] if eventos_ids else [],
            crisis_relacionadas=crisis_ids[(i - 1) % len(crisis_ids): (i - 1) % len(crisis_ids) + 1] if crisis_ids else [],
            revisiones_relacionadas=revisiones_ids[(i - 1) % len(revisiones_ids): (i - 1) % len(revisiones_ids) + 1] if revisiones_ids else [],
            riesgos_privacidad_relacionados=riesgos_ids[(i - 1) % len(riesgos_ids): (i - 1) % len(riesgos_ids) + 1] if riesgos_ids else [],
            comparativas_relacionadas=comparaciones_ids[(i - 1) % len(comparaciones_ids): (i - 1) % len(comparaciones_ids) + 1] if comparaciones_ids else [],
            accion_simulada=rng.choice(ACCIONES_SIMULADAS),
            resultado_simulado=rng.choice(RESULTADOS_SIMULADOS),
            limite_de_uso=(
                "Uso exclusivo de demo técnica sintética. No equivale a decisión empresarial real."
            ),
        )
        episodios.append(dataclass_a_dict(episodio))

    # Garantizamos al menos un episodio enlazado con crisis, privacidad y comparador para pruebas.
    if episodios and not any(ep["crisis_relacionadas"] for ep in episodios) and crisis_ids:
        episodios[0]["crisis_relacionadas"] = [crisis_ids[0]]
    if episodios and not any(ep["riesgos_privacidad_relacionados"] for ep in episodios) and riesgos_ids:
        episodios[0]["riesgos_privacidad_relacionados"] = [riesgos_ids[0]]
    if episodios and not any(ep["comparativas_relacionadas"] for ep in episodios) and comparaciones_ids:
        episodios[0]["comparativas_relacionadas"] = [comparaciones_ids[0]]

    evidencias = construir_mapa_evidencias(base_repo=base_repo)
    resumen_ejecutivo = _resumen_ejecutivo(nombre_empresa=nombre_empresa, dias=dias, contexto=contexto)
    resumen_demo = _resumen_demo(
        ficha=ficha_dict,
        hitos=hitos,
        episodios=episodios,
        evidencias=evidencias,
        contexto=contexto,
        entradas_utilizadas=entradas_utilizadas,
    )

    return {
        "ficha_narrativa_empresa": ficha_dict,
        "linea_tiempo_semanal": hitos,
        "episodios_narrativos": episodios,
        "mapa_evidencias": evidencias,
        "resumen_ejecutivo_ficticio": resumen_ejecutivo,
        "resumen_demo_narrativa": resumen_demo,
    }

