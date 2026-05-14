"""Evaluación de riesgos de privacidad simulados."""

from __future__ import annotations

from collections import Counter

from .modelos import RiesgoPrivacidad, dataclass_a_dict

SEVERIDADES = ["baja", "media", "alta", "critica"]
ESTADOS_RIESGO = ["detectado", "en_revision", "mitigado_simulado", "aceptado_simulado", "escalado"]
RECOMENDACIONES = [
    "minimizar_campos",
    "restringir_acceso",
    "anonimizar_identificadores",
    "escalar_a_responsable_privacidad",
    "revisar_permisos",
    "bloquear_uso_en_agente",
    "generar_informe_privacidad_simulado",
]


def construir_riesgos_privacidad_simulados(inventario: list[dict], matriz_permisos: list[dict], contexto: dict) -> list[dict]:
    conteo_nivel = Counter(d["nivel_sensibilidad_ficticia"] for d in inventario)
    riesgos: list[dict] = []

    riesgos_base = [
        ("exposicion_datos_confidenciales", conteo_nivel.get("confidencial", 0) > 0, "alta", "eventos,documentos"),
        ("acceso_amplio_rol_no_critico", any(p["rol"] == "agente_ia_simulado" and p["nivel_acceso"] != "sin_acceso" for p in matriz_permisos), "media", "matriz_permisos"),
        ("datos_criticos_sin_revision", any(d["nivel_sensibilidad_ficticia"] == "critica" and not d["requiere_revision_humana"] for d in inventario), "critica", "inventario"),
        ("trazabilidad_incompleta", len(contexto.get("registro_decisiones", [])) < 2, "media", "registro_decisiones"),
    ]

    idx = 1
    for tipo, condicion, severidad, origen in riesgos_base:
        if condicion:
            riesgo = RiesgoPrivacidad(
                id_riesgo=f"RGS-{idx:05d}",
                tipo_riesgo=tipo,
                descripcion="Riesgo simulado detectado por reglas de laboratorio de privacidad.",
                origen=origen,
                severidad=severidad,
                datos_afectados="inventario_sintetico",
                rol_afectado="agente_ia_simulado",
                recomendacion_simulada=RECOMENDACIONES[min(idx - 1, len(RECOMENDACIONES) - 1)],
                requiere_revision_humana=severidad in {"alta", "critica"},
                estado_riesgo="en_revision" if severidad in {"alta", "critica"} else "detectado",
            )
            riesgos.append(dataclass_a_dict(riesgo))
            idx += 1

    if not riesgos:
        riesgo = RiesgoPrivacidad(
            id_riesgo="RGS-00001",
            tipo_riesgo="seguimiento_preventivo",
            descripcion="Riesgo preventivo simulado para revisión periódica.",
            origen="fallback",
            severidad="baja",
            datos_afectados="inventario_sintetico",
            rol_afectado="responsable_datos",
            recomendacion_simulada="generar_informe_privacidad_simulado",
            requiere_revision_humana=False,
            estado_riesgo="detectado",
        )
        riesgos.append(dataclass_a_dict(riesgo))

    return riesgos
