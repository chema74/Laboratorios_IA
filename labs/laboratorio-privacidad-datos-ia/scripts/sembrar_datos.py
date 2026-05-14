import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
DATOS = BASE / "datos"


def main() -> None:
    DATOS.mkdir(parents=True, exist_ok=True)

    dataset = [
        {"id": "D-001", "texto": "Cliente NombreFicticio Uno con email nombre1@empresa.local y telefono 612345678 vive en Calle Falsa 123. ID fiscal A12345678Z.", "nombres_marcados": ["NombreFicticio Uno"]},
        {"id": "D-002", "texto": "Contacto NombreFicticio Dos: correo n2@demo.local, telefono 699998877, dirección Avenida Norte 45.", "nombres_marcados": ["NombreFicticio Dos"]},
    ]

    politicas = {
        "retencion": "Eliminar contexto sensible tras revisión técnica.",
        "minimizacion": "Incluir solo campos necesarios por caso.",
        "validacion_salida": "Bloquear PII de severidad alta.",
    }

    prompts = [
        {"caso_uso": "atencion_cliente", "objetivo": "resumen", "texto": "Resumen de cliente NombreFicticio Uno", "email": "nombre1@empresa.local", "telefono": "612345678"},
        {"caso_uso": "soporte_tic", "objetivo": "clasificar", "texto": "Ticket de NombreFicticio Dos sobre incidencia", "direccion": "Avenida Norte 45"},
    ]

    salidas = [
        {"id": "S-001", "salida": "El cliente NombreFicticio Uno tiene email nombre1@empresa.local"},
        {"id": "S-002", "salida": "Incidencia clasificada como prioritaria sin datos personales."},
    ]

    registro = {
        "finalidad": "Demostración técnica de reducción de exposición de datos sintéticos.",
        "categorias_datos": ["identificadores ficticios", "contacto ficticio"],
        "base_documental_ficticia": "POL-PRIV-001",
        "retencion_sintetica": "30 días para evidencia técnica anonimizada.",
    }

    (DATOS / "dataset_con_pii_sintetica.json").write_text(json.dumps(dataset, ensure_ascii=False, indent=2), encoding="utf-8")
    (DATOS / "politicas_privacidad_sinteticas.json").write_text(json.dumps(politicas, ensure_ascii=False, indent=2), encoding="utf-8")
    (DATOS / "prompts_con_contexto_sensible.json").write_text(json.dumps(prompts, ensure_ascii=False, indent=2), encoding="utf-8")
    (DATOS / "salidas_ia_sinteticas.json").write_text(json.dumps(salidas, ensure_ascii=False, indent=2), encoding="utf-8")
    (DATOS / "registro_tratamiento_sintetico.json").write_text(json.dumps(registro, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Datos sintéticos de privacidad creados.")


if __name__ == "__main__":
    main()
