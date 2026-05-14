import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
DATOS = BASE / "datos"


def main() -> None:
    DATOS.mkdir(parents=True, exist_ok=True)

    tareas = [
        {"id_tarea": "T-001", "titulo": "Escalado soporte TIC", "descripcion": "Coordinar respuesta a incidencia recurrente", "caso_uso": "soporte_tic"},
        {"id_tarea": "T-002", "titulo": "Revisión documental", "descripcion": "Comprobar consistencia de procedimiento interno", "caso_uso": "revision_documental"},
        {"id_tarea": "T-003", "titulo": "Seguimiento clientes", "descripcion": "Preparar seguimiento de clientes con riesgo", "caso_uso": "seguimiento_clientes"}
    ]

    herramientas = [
        {"nombre": "crm_simulado", "tipo": "consulta", "determinista": True},
        {"nombre": "gestor_tickets_simulado", "tipo": "consulta", "determinista": True},
        {"nombre": "base_documental_simulada", "tipo": "consulta", "determinista": True},
        {"nombre": "calendario_simulado", "tipo": "coordinacion", "determinista": True}
    ]

    politicas = [
        {"accion": "consultar_ticket", "permitida": True},
        {"accion": "consultar_documentacion", "permitida": True},
        {"accion": "actualizar_crm", "permitida": True},
        {"accion": "coordinar_reunion", "permitida": True},
        {"accion": "enviar_correo_real", "permitida": False},
        {"accion": "borrar_datos", "permitida": False},
        {"accion": "modificar_sistema_externo", "permitida": False},
        {"accion": "decision_legal_definitiva", "permitida": False},
        {"accion": "decision_medica_definitiva", "permitida": False},
        {"accion": "decision_financiera_definitiva", "permitida": False},
        {"accion": "ejecutar_compra_real", "permitida": False}
    ]

    escenarios = [
        {"id_escenario": "ESC-001", "id_tarea": "T-001", "tipo": "simple"},
        {"id_escenario": "ESC-002", "id_tarea": "T-002", "tipo": "multiagente"}
    ]

    (DATOS / "tareas_enterprise.json").write_text(json.dumps(tareas, ensure_ascii=False, indent=2), encoding="utf-8")
    (DATOS / "herramientas_simuladas.json").write_text(json.dumps(herramientas, ensure_ascii=False, indent=2), encoding="utf-8")
    (DATOS / "politicas_agentes.json").write_text(json.dumps(politicas, ensure_ascii=False, indent=2), encoding="utf-8")
    (DATOS / "escenarios_multiagente.json").write_text(json.dumps(escenarios, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Datos sintéticos de agentes enterprise creados.")


if __name__ == "__main__":
    main()
