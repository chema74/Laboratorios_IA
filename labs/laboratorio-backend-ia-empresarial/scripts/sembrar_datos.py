import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
DATOS = BASE / "datos"


def main() -> None:
    DATOS.mkdir(parents=True, exist_ok=True)

    contratos = {
        "/rag/consulta": ["endpoint", "metodo", "payload", "usuario", "rol", "traza_id"],
        "/evaluacion/ejecutar": ["endpoint", "metodo", "payload", "usuario", "rol", "traza_id"],
        "/privacidad/revisar": ["endpoint", "metodo", "payload", "usuario", "rol", "traza_id"],
    }

    usuarios = [
        {"usuario": "ana_admin", "rol": "admin", "token_ficticio": "tok_admin_001"},
        {"usuario": "teo_ia", "rol": "tecnico_ia", "token_ficticio": "tok_tec_001"},
        {"usuario": "aud_rosa", "rol": "auditor", "token_ficticio": "tok_aud_001"},
        {"usuario": "neg_luis", "rol": "usuario_negocio", "token_ficticio": "tok_neg_001"},
    ]

    peticiones = [
        {"endpoint": "/rag/consulta", "metodo": "POST", "payload": {"consulta": "estado de incidencias"}, "usuario": "neg_luis", "rol": "usuario_negocio", "token_ficticio": "tok_neg_001", "traza_id": "TRZ-001"},
        {"endpoint": "/privacidad/revisar", "metodo": "POST", "payload": {"texto": "cliente con datos"}, "usuario": "teo_ia", "rol": "tecnico_ia", "token_ficticio": "tok_tec_001", "traza_id": "TRZ-002"},
        {"endpoint": "/evaluacion/ejecutar", "metodo": "POST", "payload": {"caso": "C-1"}, "usuario": "aud_rosa", "rol": "auditor", "token_ficticio": "tok_aud_001", "traza_id": "TRZ-003"},
    ]

    tareas = [
        {"id": "JOB-001", "tipo": "revision_privacidad", "traza_id": "TRZ-J1", "estado": "pendiente"},
        {"id": "JOB-002", "tipo": "evaluacion_respuesta", "traza_id": "TRZ-J2", "estado": "pendiente"},
        {"id": "JOB-003", "tipo": "consulta_documental", "traza_id": "TRZ-J3", "estado": "pendiente"},
    ]

    modulos = [
        {"nombre": "rag", "simulado": True},
        {"nombre": "evaluacion", "simulado": True},
        {"nombre": "privacidad", "simulado": True},
    ]

    (DATOS / "contratos_api.json").write_text(json.dumps(contratos, ensure_ascii=False, indent=2), encoding="utf-8")
    (DATOS / "usuarios_roles.json").write_text(json.dumps(usuarios, ensure_ascii=False, indent=2), encoding="utf-8")
    (DATOS / "peticiones_backend.json").write_text(json.dumps(peticiones, ensure_ascii=False, indent=2), encoding="utf-8")
    (DATOS / "tareas_cola.json").write_text(json.dumps(tareas, ensure_ascii=False, indent=2), encoding="utf-8")
    (DATOS / "modulos_ia_empresarial.json").write_text(json.dumps(modulos, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Datos sintéticos backend creados.")


if __name__ == "__main__":
    main()
