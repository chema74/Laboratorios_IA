"""Plantillas de contenido Markdown para documentos sintéticos."""

from __future__ import annotations

from typing import Any


MAPA_CARPETAS = {
    "propuesta_comercial": "propuestas_comerciales",
    "contrato_simulado": "contratos_simulados",
    "correo_cliente": "correos_clientes",
    "acta_reunion": "actas_reunion",
    "informe_operativo": "informes_operativos",
    "ticket_soporte": "tickets_soporte",
    "politica_interna": "politicas_internas",
}


def construir_markdown_documento(meta: dict[str, Any], cuerpo: str) -> str:
    return (
        f"# {meta['titulo']}\n\n"
        "**Aviso:** Este es un documento sintético generado para pruebas internas del laboratorio. "
        "No corresponde a una operación real ni a una entidad real.\n\n"
        "## Metadatos\n"
        f"- id_documento: {meta['id_documento']}\n"
        f"- tipo_documento: {meta['tipo_documento']}\n"
        f"- fecha_documento: {meta['fecha_documento']}\n"
        f"- entidad_relacionada: {meta['entidad_relacionada']}\n"
        f"- id_entidad_relacionada: {meta['id_entidad_relacionada']}\n"
        f"- origen_simulado: {meta['origen_simulado']}\n"
        f"- nivel_sensibilidad_ficticia: {meta['nivel_sensibilidad_ficticia']}\n"
        f"- requiere_revision_humana: {meta['requiere_revision_humana']}\n"
        f"- estado_documento: {meta['estado_documento']}\n\n"
        "## Cuerpo del documento\n"
        f"{cuerpo}\n\n"
        "## Limites\n"
        "- Documento de uso técnico, no legal ni contractual real.\n"
        "- No sustituye revisión profesional humana.\n"
        "- No utiliza datos reales.\n\n"
        "## Uso previsto en el laboratorio\n"
        "Soporte para pruebas de flujos operativos, trazabilidad y evaluación de agentes en entorno local.\n"
    )


def construir_cuerpo(tipo: str, empresa_nombre: str, cliente_id: str, evento_tipo: str) -> str:
    if tipo == "propuesta_comercial":
        return f"Se propone un servicio sintético para {cliente_id} de {empresa_nombre}, con alcance operativo y validación interna."
    if tipo == "contrato_simulado":
        return (
            "Documento simulado de condiciones comerciales internas. "
            "No es un contrato real, no tiene validez legal y no constituye asesoramiento jurídico."
        )
    if tipo == "correo_cliente":
        return f"Mensaje sintético al cliente {cliente_id} relacionado con el evento {evento_tipo}."
    if tipo == "acta_reunion":
        return f"Acta ficticia de seguimiento operativo sobre incidencias y acciones de {empresa_nombre}."
    if tipo == "informe_operativo":
        return "Informe sintético de eventos, pagos pendientes, incidencias activas y alertas operativas observadas."
    if tipo == "ticket_soporte":
        return f"Ticket ficticio abierto por evento {evento_tipo} para la entidad {cliente_id}."
    return "Política interna ficticia sobre uso de datos sintéticos y revisión humana de salidas automatizadas."
