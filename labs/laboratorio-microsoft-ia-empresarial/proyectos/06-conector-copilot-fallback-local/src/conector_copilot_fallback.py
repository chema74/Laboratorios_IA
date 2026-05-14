import argparse
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

CAMPOS_OBLIGATORIOS = [
    "id_solicitud",
    "tipo_solicitud",
    "contexto_sintetico",
    "prompt_simulado_no_real",
    "entrada_sintetica",
    "respuesta_esperada_simulada",
    "requiere_copilot_real",
    "fallback_obligatorio",
    "razon_fallback",
    "sensibilidad_simulada",
    "origen_simulado",
    "limites_declarados",
    "usa_copilot_real",
    "usa_microsoft_graph_real",
    "usa_api_externa",
    "usa_azure",
    "usa_ia_real",
    "nota_sintetica",
]


def cargar_json(ruta: Path) -> dict:
    with ruta.open("r", encoding="utf-8") as f:
        return json.load(f)


def validar_config(config: dict) -> None:
    if config.get("modo_v1") != "fallback-local":
        raise ValueError("modo_v1 debe ser fallback-local.")
    if config.get("permitir_copilot_real") is not False:
        raise ValueError("Copilot real debe estar desactivado.")
    if config.get("permitir_microsoft_graph_real") is not False:
        raise ValueError("Microsoft Graph API real debe estar desactivado.")


def validar_solicitudes(solicitudes: list[dict], config: dict) -> None:
    tipos = set(config["tipos_solicitud_permitidos"])
    origenes = {"outlook", "word", "excel", "teams", "planner", "onedrive", "microsoft365_conceptual"}
    for i, s in enumerate(solicitudes, start=1):
        faltantes = [c for c in CAMPOS_OBLIGATORIOS if c not in s]
        if faltantes:
            raise ValueError(f"Solicitud {i} invalida: faltan {faltantes}")
        if s["tipo_solicitud"] not in tipos:
            raise ValueError(f"Tipo solicitud no permitido: {s['id_solicitud']}")
        if s["origen_simulado"] not in origenes:
            raise ValueError(f"Origen no permitido: {s['id_solicitud']}")
        if s["fallback_obligatorio"] is not True:
            raise ValueError(f"{s['id_solicitud']} debe activar fallback obligatorio.")
        if s["requiere_copilot_real"] is not False:
            raise ValueError(f"{s['id_solicitud']} no puede requerir Copilot real.")
        for b in ["usa_copilot_real", "usa_microsoft_graph_real", "usa_api_externa", "usa_azure", "usa_ia_real"]:
            if s[b] is not False:
                raise ValueError(f"{s['id_solicitud']} incumple politica en {b}")


def respuesta_fallback_determinista(tipo_solicitud: str, entrada: str, max_palabras: int) -> str:
    plantillas = {
        "resumen de correo ficticio": "Resumen local: priorizar respuesta y seguimiento interno simulado.",
        "resumen de documento Word sintético": "Resumen local: extraer puntos clave documentales y riesgos simulados.",
        "análisis de libro Excel simulado": "Analisis local: revisar margen simulado, alertas y registros de revision.",
        "propuesta de respuesta empresarial": "Propuesta local: respuesta profesional breve con siguientes pasos simulados.",
        "resumen de reunión Teams simulada": "Resumen local: acuerdos, responsables ficticios y pendientes simulados.",
        "generación de tarea Planner simulada": "Tarea local: crear seguimiento con prioridad y fecha simulada.",
        "explicación de alerta ficticia": "Explicacion local: causa probable simulada y accion correctiva sugerida.",
        "recomendación operativa simulada": "Recomendacion local: optimizar flujo, trazabilidad y control de bloqueos.",
    }
    base = plantillas.get(tipo_solicitud, "Respuesta local simulada de fallback.")
    texto = f"{base} Entrada sintetica: {entrada}"
    palabras = texto.split()
    return " ".join(palabras[:max_palabras]) + ("..." if len(palabras) > max_palabras else "")


def guardar_registro(responses_dir: Path, resultado: dict) -> str:
    responses_dir.mkdir(parents=True, exist_ok=True)
    ruta = responses_dir / f"{resultado['id_solicitud']}.json"
    ruta.write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(ruta)


def generar_informe_md(resultados: list[dict], config: dict) -> str:
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    por_tipo = Counter(r["tipo_solicitud"] for r in resultados)
    por_origen = Counter(r["origen_simulado"] for r in resultados)
    por_razon = Counter(r["razon_fallback"] for r in resultados)
    md = [
        "# Informe Conector Copilot con Fallback Local (V1)",
        "",
        f"Fecha de generación: {fecha}",
        "",
        "## Resumen ejecutivo",
        "Conector conceptual ejecutado en modo fallback-local determinista, sin Copilot real ni APIs reales.",
        "",
        "## Total de solicitudes",
        f"- {len(resultados)}",
        "",
        "## Solicitudes por tipo",
    ]
    for k in sorted(por_tipo):
        md.append(f"- {k}: {por_tipo[k]}")
    md.extend(["", "## Solicitudes por origen"])
    for k in sorted(por_origen):
        md.append(f"- {k}: {por_origen[k]}")
    md.extend(["", "## Motivos de fallback"])
    for k in sorted(por_razon):
        md.append(f"- {k}: {por_razon[k]}")
    md.extend(["", "## Respuestas simuladas generadas"])
    for r in resultados[:4]:
        md.append(f"- {r['id_solicitud']}: {r['respuesta_simulada']}")
    md.extend(["", "## Trazabilidad de fallback"])
    for r in resultados[:4]:
        md.append(f"- {r['id_solicitud']}: {r['trazabilidad_fallback']}")
    md.extend(
        [
            "",
            "## Límites de la V1",
            "- Sin Copilot real.",
            "- Sin Microsoft Graph API real.",
            "- Sin OAuth real ni claves reales.",
            "- Sin Azure obligatorio.",
            "- Sin IA real y sin red.",
            "",
            "## Posible V2 futura con .env y fallback local",
            "- Integración opcional controlada mediante variables de entorno.",
            "- El fallback local permanece obligatorio como mecanismo de continuidad.",
            "",
            "## Recomendaciones siguientes",
            "- Versionar reglas de respuesta fallback por tipo de solicitud.",
            "- Añadir validaciones de contrato para integración opcional V2.",
            "- Mantener trazabilidad por solicitud.",
            "",
            "## 🪪 Licencia y Autoría",
            "Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  ",
            "© 2025 – Txema Ríos. Todos los derechos compartidos.",
            "",
        ]
    )
    return "\n".join(md)


def ejecutar(requests_path: Path, config_path: Path, output_md: Path, output_json: Path, responses_dir: Path) -> dict:
    data = cargar_json(requests_path)
    config = cargar_json(config_path)
    validar_config(config)
    solicitudes = data.get("solicitudes", [])
    if not solicitudes:
        raise ValueError("No hay solicitudes para procesar.")
    validar_solicitudes(solicitudes, config)

    max_palabras = int(config["reglas_respuesta_fallback"]["max_palabras"])
    resultados = []
    for s in solicitudes:
        respuesta = respuesta_fallback_determinista(s["tipo_solicitud"], s["entrada_sintetica"], max_palabras)
        trazabilidad = f"fallback-local|{s['id_solicitud']}|{datetime.now().isoformat(timespec='seconds')}|sin-red"
        res = {
            "id_solicitud": s["id_solicitud"],
            "tipo_solicitud": s["tipo_solicitud"],
            "origen_simulado": s["origen_simulado"],
            "modo_ejecucion": "fallback-local",
            "respuesta_simulada": respuesta,
            "razon_fallback": s["razon_fallback"],
            "trazabilidad_fallback": trazabilidad,
            "registro_generado": "",
            "usa_copilot_real": False,
            "usa_microsoft_graph_real": False,
            "usa_api_externa": False,
            "usa_azure": False,
            "usa_ia_real": False,
        }
        res["registro_generado"] = guardar_registro(responses_dir, res)
        resultados.append(res)

    salida = {
        "metadata": {
            "fecha_generacion": datetime.now().isoformat(timespec="seconds"),
            "total_solicitudes": len(resultados),
            "modo_v1": config["modo_v1"],
            "nota": config.get("nota", ""),
        },
        "resumen_por_tipo_solicitud": dict(Counter(r["tipo_solicitud"] for r in resultados)),
        "resumen_por_origen": dict(Counter(r["origen_simulado"] for r in resultados)),
        "resumen_por_razon_fallback": dict(Counter(r["razon_fallback"] for r in resultados)),
        "resultados": resultados,
    }
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(generar_informe_md(resultados, config), encoding="utf-8")
    output_json.write_text(json.dumps(salida, ensure_ascii=False, indent=2), encoding="utf-8")
    return salida


def crear_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Conector conceptual Copilot con fallback local.")
    p.add_argument("--requests", required=True, type=Path)
    p.add_argument("--config", required=True, type=Path)
    p.add_argument("--output-md", required=True, type=Path)
    p.add_argument("--output-json", required=True, type=Path)
    p.add_argument("--responses-dir", required=True, type=Path)
    return p


def main() -> None:
    args = crear_parser().parse_args()
    ejecutar(args.requests, args.config, args.output_md, args.output_json, args.responses_dir)


if __name__ == "__main__":
    main()
