"""Generación determinista de documentos empresariales sintéticos."""

from __future__ import annotations

import random
from collections import Counter
from datetime import date

from .modelos import DocumentoSintetico, ResumenDocumentos, dataclass_a_dict
from .plantillas_documentos import MAPA_CARPETAS, construir_cuerpo, construir_markdown_documento

TIPOS_DOCUMENTO = list(MAPA_CARPETAS.keys())


def _seleccionar(azar: random.Random, opciones: list[str]) -> str:
    return opciones[azar.randrange(0, len(opciones))]


def generar_documentos_sinteticos(contexto: dict, seed: int = 42, documentos_por_tipo: int = 2) -> list[dict]:
    """
    1) Reutiliza empresa y eventos del contexto.
    2) Genera documentos por cada tipo mínimo obligatorio.
    3) Construye contenido Markdown con aviso y metadatos visibles.
    """
    azar = random.Random(seed)
    hoy = date.today().isoformat()

    empresa = contexto.get("empresa", {})
    bloque_empresa = empresa.get("empresa", {}) if isinstance(empresa, dict) else {}
    empresa_nombre = bloque_empresa.get("nombre", "Empresa Sintetica Fallback")

    clientes = empresa.get("clientes", []) if isinstance(empresa, dict) else []
    if not clientes:
        clientes = [{"id_cliente": "CLI-0001"}]

    eventos = contexto.get("eventos", []) if isinstance(contexto.get("eventos", []), list) else []
    if not eventos:
        eventos = [{"tipo_evento": "pedido_creado", "id_entidad_afectada": "CLI-0001", "requiere_revision_humana": False}]

    documentos: list[dict] = []
    indice = 1

    for tipo in TIPOS_DOCUMENTO:
        carpeta = MAPA_CARPETAS[tipo]
        for n in range(1, documentos_por_tipo + 1):
            cliente = clientes[(indice - 1) % len(clientes)]
            evento = eventos[(indice - 1) % len(eventos)]
            cliente_id = cliente.get("id_cliente", "CLI-0001")
            evento_tipo = evento.get("tipo_evento", "evento_desconocido")

            meta = {
                "id_documento": f"DOC-{indice:06d}",
                "tipo_documento": tipo,
                "titulo": f"{tipo.replace('_', ' ').title()} {n}",
                "fecha_documento": hoy,
                "entidad_relacionada": "cliente" if "cliente" in tipo or tipo in {"propuesta_comercial", "contrato_simulado"} else "operacion",
                "id_entidad_relacionada": cliente_id,
                "origen_simulado": "fabrica_documentos_sinteticos_v1_local",
                "nivel_sensibilidad_ficticia": _seleccionar(azar, ["bajo", "medio", "alto"]),
                "requiere_revision_humana": bool(evento.get("requiere_revision_humana", False) or tipo in {"contrato_simulado", "politica_interna"}),
                "ruta_markdown": f"{carpeta}/DOC-{indice:06d}.md",
                "estado_documento": _seleccionar(azar, ["borrador", "en_revision", "aprobado"]),
            }

            cuerpo = construir_cuerpo(tipo, empresa_nombre, cliente_id, evento_tipo)
            markdown = construir_markdown_documento(meta, cuerpo)

            doc = DocumentoSintetico(contenido_markdown=markdown, **meta)
            documentos.append(dataclass_a_dict(doc))
            indice += 1

    return documentos


def construir_resumen_documentos(documentos: list[dict], entradas_utilizadas: dict[str, str]) -> dict:
    tipos = Counter(d["tipo_documento"] for d in documentos)
    niveles = Counter(d["nivel_sensibilidad_ficticia"] for d in documentos)
    revisiones = sum(1 for d in documentos if d.get("requiere_revision_humana"))

    resumen = ResumenDocumentos(
        total_documentos=len(documentos),
        documentos_por_tipo=dict(tipos),
        documentos_que_requieren_revision_humana=revisiones,
        niveles_sensibilidad_ficticia=dict(niveles),
        fecha_generacion=date.today().isoformat(),
        entradas_utilizadas=entradas_utilizadas,
        advertencia_sobre_datos_sinteticos="Contenido sintético para pruebas internas. No usar como documento real.",
    )
    return dataclass_a_dict(resumen)
