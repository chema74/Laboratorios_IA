"""Matriz de permisos simulados para datos sintéticos."""

from __future__ import annotations

ROLES = [
    "direccion",
    "responsable_operaciones",
    "responsable_comercial",
    "responsable_datos",
    "responsable_privacidad",
    "responsable_tecnico",
    "auditor_simulado",
    "agente_ia_simulado",
]

NIVELES_ACCESO = ["sin_acceso", "lectura_minima", "lectura_operativa", "lectura_ampliada", "revision_controlada"]


def _nivel_para_rol_y_sensibilidad(rol: str, nivel: str) -> str:
    if rol == "agente_ia_simulado" and nivel in {"confidencial", "critica"}:
        return "sin_acceso"
    if rol == "responsable_privacidad":
        return "revision_controlada" if nivel == "critica" else "lectura_ampliada"
    if rol == "direccion":
        return "lectura_ampliada" if nivel in {"interna", "confidencial"} else "lectura_operativa"
    if nivel == "critica":
        return "lectura_minima"
    if nivel == "confidencial":
        return "lectura_operativa"
    return "lectura_minima"


def construir_matriz_permisos_simulados(inventario: list[dict]) -> list[dict]:
    tipos_entidad = sorted({d["tipo_entidad"] for d in inventario}) or ["general"]
    salida: list[dict] = []
    idx = 1

    for rol in ROLES:
        for tipo in tipos_entidad:
            subset = [d for d in inventario if d["tipo_entidad"] == tipo]
            niveles = sorted({d["nivel_sensibilidad_ficticia"] for d in subset}) or ["interna"]
            nivel_predominante = niveles[-1]
            nivel_acceso = _nivel_para_rol_y_sensibilidad(rol, nivel_predominante)

            permitidos = sorted({d["campo"] for d in subset if d["nivel_sensibilidad_ficticia"] in {"publica", "interna"}})[:8]
            restringidos = sorted({d["campo"] for d in subset if d["nivel_sensibilidad_ficticia"] in {"confidencial", "critica"}})[:8]

            salida.append(
                {
                    "id_permiso": f"PER-{idx:05d}",
                    "rol": rol,
                    "tipo_entidad": tipo,
                    "nivel_acceso": nivel_acceso,
                    "campos_permitidos": ",".join(permitidos) if permitidos else "sin_campos",
                    "campos_restringidos": ",".join(restringidos) if restringidos else "sin_restricciones",
                    "justificacion_simulada": "Asignación simulada por nivel de sensibilidad ficticia.",
                    "requiere_aprobacion_humana": nivel_acceso in {"sin_acceso", "revision_controlada"},
                }
            )
            idx += 1

    return salida
