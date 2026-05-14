import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
DATOS = BASE / "datos"


def main() -> None:
    DATOS.mkdir(parents=True, exist_ok=True)

    dataset = [
        {"id": "CASO-001", "consulta": "Plazo de respuesta al cliente", "respuesta_esperada": "Según el procedimiento de atención al cliente, el plazo máximo de primera respuesta es de 24 horas laborables.", "criterios_clave": ["24 horas", "primera respuesta", "atención al cliente"], "riesgos": ["prometer plazos falsos"], "categoria": "atencion_cliente"},
        {"id": "CASO-002", "consulta": "Aprobación de compras TIC", "respuesta_esperada": "Según política de compras, adquisiciones TIC superiores a 2000 euros requieren validación de área y finanzas.", "criterios_clave": ["2000 euros", "validación", "finanzas"], "riesgos": ["saltarse aprobaciones"], "categoria": "compras"},
        {"id": "CASO-003", "consulta": "Rotación de contraseñas", "respuesta_esperada": "La política interna indica rotación trimestral para perfiles privilegiados y semestral para perfiles estándar.", "criterios_clave": ["trimestral", "semestral", "perfiles privilegiados"], "riesgos": ["incumplimiento seguridad"], "categoria": "cumplimiento"},
        {"id": "CASO-004", "consulta": "SLA de soporte TIC", "respuesta_esperada": "El soporte TIC define 30 minutos para incidencias críticas y 4 horas para incidencias medias.", "criterios_clave": ["30 minutos", "4 horas", "incidencias críticas"], "riesgos": ["escalado tardío"], "categoria": "soporte_tic"},
        {"id": "CASO-005", "consulta": "Solicitud de vacaciones", "respuesta_esperada": "RRHH exige solicitar vacaciones con 15 días de antelación y registro en portal interno.", "criterios_clave": ["15 días", "portal interno", "RRHH"], "riesgos": ["conflictos operativos"], "categoria": "recursos_humanos"},
        {"id": "CASO-006", "consulta": "Norma de cumplimiento documental", "respuesta_esperada": "Cumplimiento requiere conservar evidencias de auditoría por 24 meses según norma interna.", "criterios_clave": ["24 meses", "auditoría", "norma interna"], "riesgos": ["sanción regulatoria"], "categoria": "cumplimiento"},
    ]

    respuestas = [
        {"respuesta_id": "R-001-A", "caso_id": "CASO-001", "modelo_sintetico": "modelo_alpha", "respuesta": "Según atención al cliente, la primera respuesta debe darse en 24 horas laborables."},
        {"respuesta_id": "R-001-B", "caso_id": "CASO-001", "modelo_sintetico": "modelo_beta", "respuesta": "Siempre respondemos en 12 horas y en todos los casos."},
        {"respuesta_id": "R-002-A", "caso_id": "CASO-002", "modelo_sintetico": "modelo_alpha", "respuesta": "Según política de compras, más de 2000 euros requiere validación de área y finanzas."},
        {"respuesta_id": "R-003-A", "caso_id": "CASO-003", "modelo_sintetico": "modelo_alpha", "respuesta": "La rotación es trimestral para perfiles privilegiados y semestral para estándar."},
        {"respuesta_id": "R-004-A", "caso_id": "CASO-004", "modelo_sintetico": "modelo_alpha", "respuesta": "Soporte TIC: críticas 30 minutos y medias 4 horas."},
        {"respuesta_id": "R-005-A", "caso_id": "CASO-005", "modelo_sintetico": "modelo_alpha", "respuesta": "RRHH pide 15 días de antelación y registro en portal interno."},
        {"respuesta_id": "R-006-A", "caso_id": "CASO-006", "modelo_sintetico": "modelo_alpha", "respuesta": "Cumplimiento conserva evidencias de auditoría por 24 meses según norma interna."},
    ]

    prompts = [
        {"caso_id": "CASO-002", "version": "v1", "prompt": "Responder compras con detalle", "respuesta_sintetica": "Compras TIC de 2000 euros requiere validación y finanzas."},
        {"caso_id": "CASO-002", "version": "v2", "prompt": "Responder compras breve", "respuesta_sintetica": "Compras TIC requiere validación."},
        {"caso_id": "CASO-004", "version": "v1", "prompt": "Responder SLA soporte", "respuesta_sintetica": "Críticas 30 minutos y medias 4 horas."},
        {"caso_id": "CASO-004", "version": "v2", "prompt": "Responder SLA soporte simplificado", "respuesta_sintetica": "Críticas 30 minutos y medias 4 horas."}
    ]

    (DATOS / "dataset_dorado.json").write_text(json.dumps(dataset, ensure_ascii=False, indent=2), encoding="utf-8")
    (DATOS / "respuestas_sinteticas.json").write_text(json.dumps(respuestas, ensure_ascii=False, indent=2), encoding="utf-8")
    (DATOS / "prompts_versionados.json").write_text(json.dumps(prompts, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Datos sintéticos sembrados correctamente.")


if __name__ == "__main__":
    main()
