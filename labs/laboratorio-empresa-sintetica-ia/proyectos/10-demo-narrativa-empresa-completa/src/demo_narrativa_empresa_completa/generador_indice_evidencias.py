"""Generación del mapa de evidencias de proyectos previos."""

from __future__ import annotations

from pathlib import Path

from .modelos import EvidenciaMapa, dataclass_a_dict


CATALOGO_EVIDENCIAS = [
    ("01-generador-empresa-sintetica", "empresa_json", "datos_ejemplo/empresa_sintetica_demo/empresa_sintetica.json", "Ficha general de la empresa sintética base."),
    ("01-generador-empresa-sintetica", "clientes_csv", "datos_ejemplo/empresa_sintetica_demo/clientes.csv", "Listado sintético de clientes para alimentar simulaciones."),
    ("02-simulador-eventos-negocio", "eventos_json", "datos_ejemplo/eventos_negocio_demo/eventos_negocio.json", "Eventos de negocio simulados de la semana."),
    ("02-simulador-eventos-negocio", "resumen_eventos", "datos_ejemplo/eventos_negocio_demo/resumen_eventos.json", "Resumen agregado de actividad de eventos."),
    ("03-fabrica-documentos-sinteticos", "indice_documentos", "datos_ejemplo/documentos_sinteticos_demo/indice_documentos.json", "Índice de documentos empresariales sintéticos."),
    ("04-generador-escenarios-prueba-agentes", "escenarios_json", "datos_ejemplo/escenarios_prueba_agentes_demo/escenarios_prueba_agentes.json", "Escenarios de evaluación futura de agentes simulados."),
    ("05-motor-simulacion-crisis", "crisis_json", "datos_ejemplo/crisis_simuladas_demo/crisis_simuladas.json", "Registro de crisis empresariales sintéticas."),
    ("06-simulador-revision-humana", "revisiones_json", "datos_ejemplo/revision_humana_demo/revisiones_humanas.json", "Revisiones humanas simuladas sobre artefactos."),
    ("07-gemelo-digital-operativo-ligero", "estado_operativo", "datos_ejemplo/gemelo_digital_operativo_demo/estado_operativo.json", "Estado operativo consolidado del gemelo digital sintético."),
    ("08-laboratorio-privacidad-datos-sinteticos", "riesgos_privacidad", "datos_ejemplo/privacidad_datos_sinteticos_demo/riesgos_privacidad_simulados.json", "Riesgos de privacidad simulados sobre datos sintéticos."),
    ("09-comparador-agente-proceso", "comparaciones", "datos_ejemplo/comparador_agente_proceso_demo/comparaciones_agente_proceso.json", "Comparación simulada entre flujos manuales y asistidos."),
]


def construir_mapa_evidencias(base_repo: Path) -> list[dict]:
    evidencias: list[dict] = []

    # 1) Recorremos el catálogo mínimo de artefactos clave del laboratorio.
    # 2) Solo añadimos los que existen en disco para mantener trazabilidad real.
    # 3) Cada entrada deja explícito que su uso es sintético para demo técnica.
    for i, (proyecto, tipo, ruta, descripcion) in enumerate(CATALOGO_EVIDENCIAS, start=1):
        if not (base_repo / ruta).exists():
            continue
        evidencia = EvidenciaMapa(
            id_evidencia=f"EVD-{i:04d}",
            proyecto_origen=proyecto,
            tipo_evidencia=tipo,
            ruta_relativa=ruta,
            descripcion=descripcion,
            uso_en_demo="Apoyo narrativo y técnico para explicar integración de proyectos 01 a 10.",
            es_sintetica=True,
        )
        evidencias.append(dataclass_a_dict(evidencia))

    return evidencias

