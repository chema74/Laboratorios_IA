import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
RUTA = BASE / "datos" / "brutos" / "documentos_corporativos.json"


def crear_documentos_sinteticos() -> list[dict]:
    return [
        {"id": "DOC-001", "titulo": "Política de teletrabajo", "area": "recursos_humanos", "etiquetas": ["rrhh", "teletrabajo", "jornada"], "contenido": "La política de teletrabajo establece tres días remotos por semana para perfiles elegibles. El registro horario se realiza en portal interno y las incidencias deben notificarse al responsable de equipo en menos de 24 horas."},
        {"id": "DOC-002", "titulo": "Procedimiento de compras TIC", "area": "compras", "etiquetas": ["compras", "proveedores", "tic"], "contenido": "Toda compra TIC superior a 2000 euros requiere doble validación: responsable de área y finanzas. El proveedor debe estar homologado y el expediente debe incluir comparativa de al menos dos ofertas."},
        {"id": "DOC-003", "titulo": "Protocolo de soporte interno", "area": "soporte", "etiquetas": ["soporte", "incidencias", "sla"], "contenido": "Las incidencias críticas tienen SLA de primera respuesta de 30 minutos. Las incidencias medias tienen SLA de 4 horas. El cierre requiere confirmación del solicitante o cierre automático tras 72 horas sin respuesta."},
        {"id": "DOC-004", "titulo": "Norma de seguridad de contraseñas", "area": "seguridad", "etiquetas": ["seguridad", "accesos", "password"], "contenido": "Las contraseñas corporativas deben tener mínimo 12 caracteres y combinar mayúsculas, minúsculas, números y símbolo. La rotación es trimestral para perfiles privilegiados y semestral para perfiles estándar."},
        {"id": "DOC-005", "titulo": "Procedimiento de operaciones de backup", "area": "operaciones", "etiquetas": ["operaciones", "backup", "continuidad"], "contenido": "Los backups incrementales se ejecutan diariamente a las 23:00 y el backup completo semanal los domingos. La restauración de prueba se valida una vez al mes y se documenta en el registro de continuidad."},
        {"id": "DOC-006", "titulo": "Política de vacaciones y permisos", "area": "recursos_humanos", "etiquetas": ["rrhh", "vacaciones", "permisos"], "contenido": "Las solicitudes de vacaciones deben registrarse con al menos 15 días de antelación. Los permisos retribuidos se justifican documentalmente en las 48 horas siguientes al evento."},
    ]


def main() -> None:
    RUTA.parent.mkdir(parents=True, exist_ok=True)
    docs = crear_documentos_sinteticos()
    with RUTA.open("w", encoding="utf-8") as f:
        json.dump(docs, f, ensure_ascii=False, indent=2)
    print(f"Datos sintéticos creados: {RUTA} ({len(docs)} documentos)")


if __name__ == "__main__":
    main()
