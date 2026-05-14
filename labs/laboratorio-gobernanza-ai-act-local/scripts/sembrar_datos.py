import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
DATOS = BASE / "datos"


def main() -> None:
    DATOS.mkdir(parents=True, exist_ok=True)

    casos = [
        {"identificador": "CU-001", "nombre": "Asistente RRHH", "area": "recursos_humanos", "descripcion": "Asistencia en cribado de solicitudes internas", "usuarios_afectados": "empleados", "datos_tratados": "datos laborales", "criticidad": "media", "grado_automatizacion": "medio", "supervision_humana": "alta", "impacto_potencial": "medio", "evidencias_asociadas": ["E-001", "E-002"]},
        {"identificador": "CU-002", "nombre": "Clasificación tickets TI", "area": "soporte_tic", "descripcion": "Prioriza incidencias técnicas", "usuarios_afectados": "usuarios internos", "datos_tratados": "logs operativos", "criticidad": "alta", "grado_automatizacion": "alto", "supervision_humana": "baja", "impacto_potencial": "alto", "evidencias_asociadas": ["E-003"]},
        {"identificador": "CU-003", "nombre": "Resumen atención cliente", "area": "atencion_cliente", "descripcion": "Resume interacciones para seguimiento", "usuarios_afectados": "clientes", "datos_tratados": "datos de contacto", "criticidad": "media", "grado_automatizacion": "medio", "supervision_humana": "media", "impacto_potencial": "medio", "evidencias_asociadas": ["E-004"]},
        {"identificador": "CU-004", "nombre": "Predicción ventas", "area": "ventas", "descripcion": "Proyección orientativa de demanda", "usuarios_afectados": "equipo comercial", "datos_tratados": "datos comerciales agregados", "criticidad": "baja", "grado_automatizacion": "bajo", "supervision_humana": "alta", "impacto_potencial": "bajo", "evidencias_asociadas": ["E-005"]},
        {"identificador": "CU-005", "nombre": "Análisis directivo", "area": "analisis_directivo", "descripcion": "Informe sintético para comité", "usuarios_afectados": "dirección", "datos_tratados": "datos sensibles financieros", "criticidad": "alta", "grado_automatizacion": "alto", "supervision_humana": "media", "impacto_potencial": "alto", "evidencias_asociadas": ["E-006"]}
    ]

    matriz = {"riesgo mínimo": ["documentación mínima", "revisión periódica"], "riesgo limitado": ["documentación mínima", "comunicación a usuarios", "trazabilidad"], "riesgo alto orientativo": ["documentación mínima", "supervisión humana", "trazabilidad", "validación de datos", "revisión periódica"], "revisión obligatoria": ["documentación mínima", "supervisión humana", "trazabilidad", "comunicación a usuarios", "revisión periódica", "validación de datos"]}

    obligaciones = matriz

    evidencias = {
        "CU-001": {"responsable": "Resp. RRHH", "descripcion_funcional": True, "datos_tratados": True, "revision_humana": True, "trazabilidad": True, "politica_interna": True},
        "CU-002": {"responsable": "Resp. TI", "descripcion_funcional": True, "datos_tratados": True, "revision_humana": False, "trazabilidad": True, "politica_interna": True},
        "CU-003": {"responsable": "Resp. CX", "descripcion_funcional": True, "datos_tratados": True, "revision_humana": True, "trazabilidad": False, "politica_interna": True},
        "CU-004": {"responsable": "Resp. Ventas", "descripcion_funcional": True, "datos_tratados": True, "revision_humana": True, "trazabilidad": True, "politica_interna": True},
        "CU-005": {"responsable": "Resp. Dirección", "descripcion_funcional": True, "datos_tratados": True, "revision_humana": True, "trazabilidad": True, "politica_interna": False}
    }

    shadow = [
        {"id": "S-001", "descripcion": "Uso no registrado de IA generativa en informes", "declarado": False, "documentacion": "baja", "impacto": "alto"},
        {"id": "S-002", "descripcion": "Macro local con IA para clasificar correos", "declarado": True, "documentacion": "baja", "impacto": "medio"}
    ]

    (DATOS / "casos_uso_ia.json").write_text(json.dumps(casos, ensure_ascii=False, indent=2), encoding="utf-8")
    (DATOS / "matriz_riesgos.json").write_text(json.dumps(matriz, ensure_ascii=False, indent=2), encoding="utf-8")
    (DATOS / "obligaciones_orientativas.json").write_text(json.dumps(obligaciones, ensure_ascii=False, indent=2), encoding="utf-8")
    (DATOS / "evidencias_gobernanza.json").write_text(json.dumps(evidencias, ensure_ascii=False, indent=2), encoding="utf-8")
    (DATOS / "shadow_ia_sintetica.json").write_text(json.dumps(shadow, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Datos sintéticos de gobernanza creados.")


if __name__ == "__main__":
    main()
