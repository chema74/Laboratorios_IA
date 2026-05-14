"""Simulador local de flujo Gmail empresarial con IA sintética."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

CAMPOS_CORREO = {
    "id_correo",
    "remitente_ficticio",
    "destinatario_ficticio",
    "asunto",
    "cuerpo_sintetico",
    "fecha_simulada",
    "categoria_esperada",
    "prioridad_esperada",
    "requiere_respuesta",
    "requiere_tarea",
    "sensibilidad_simulada",
    "accion_recomendada_esperada",
    "limites_declarados",
    "usa_gmail_real",
    "usa_oauth_real",
    "usa_api_externa",
    "usa_cloud",
    "usa_ia_real",
    "nota_sintetica",
}


def cargar_json(ruta: Path) -> dict:
    with ruta.open("r", encoding="utf-8-sig") as archivo:
        return json.load(archivo)


def validar_correos(correos: list[dict], config: dict) -> None:
    if not correos:
        raise ValueError("No hay correos sintéticos para procesar.")
    categorias = set(config.get("categorias_permitidas", []))
    prioridades = set(config.get("prioridades_permitidas", []))
    for indice, correo in enumerate(correos, start=1):
        faltantes = CAMPOS_CORREO.difference(correo.keys())
        if faltantes:
            raise ValueError(f"Correo {indice} incompleto: faltan {sorted(faltantes)}")
        if correo["categoria_esperada"] not in categorias:
            raise ValueError(f"Categoría esperada inválida en {correo['id_correo']}")
        if correo["prioridad_esperada"] not in prioridades:
            raise ValueError(f"Prioridad esperada inválida en {correo['id_correo']}")


def _buscar(texto: str, reglas: dict[str, list[str]], predeterminado: str) -> str:
    valor = texto.lower()
    for etiqueta, palabras in reglas.items():
        if any(p.lower() in valor for p in palabras):
            return etiqueta
    return predeterminado


def detectar_categoria(correo: dict, reglas: dict[str, list[str]]) -> str:
    return _buscar(f"{correo['asunto']} {correo['cuerpo_sintetico']}", reglas, "otros")


def detectar_prioridad(correo: dict) -> str:
    texto = f"{correo['asunto']} {correo['cuerpo_sintetico']}".lower()
    if "urgente" in texto or correo["prioridad_esperada"] == "alta":
        return "alta"
    if correo["prioridad_esperada"] == "media":
        return "media"
    return "baja"


def detectar_sensibilidad(correo: dict, reglas: dict[str, list[str]]) -> str:
    return _buscar(f"{correo['asunto']} {correo['cuerpo_sintetico']}", reglas, correo["sensibilidad_simulada"])


def detectar_requiere_tarea(correo: dict, config: dict) -> bool:
    claves = config.get("reglas_tarea_simulada", {}).get("crear_si_contiene", [])
    texto = f"{correo['asunto']} {correo['cuerpo_sintetico']}".lower()
    return correo["requiere_tarea"] or any(k.lower() in texto for k in claves)


def generar_respuesta(correo: dict, categoria: str, prioridad: str, config: dict) -> str:
    regla = config.get("reglas_respuesta_simulada", {}).get(prioridad, "Respuesta simulada estándar.")
    return f"[SIMULADO] {correo['id_correo']} ({categoria}): {regla} Sin Gmail real ni IA real."


def generar_tarea(correo: dict, requiere_tarea: bool) -> str:
    if not requiere_tarea:
        return ""
    return f"[SIMULADO] Crear tarea de seguimiento para {correo['id_correo']} sobre '{correo['asunto']}'."


def generar_registro(mailbox_dir: Path, resultado: dict) -> str:
    mailbox_dir.mkdir(parents=True, exist_ok=True)
    ruta = mailbox_dir / f"{resultado['id_correo']}.json"
    ruta.write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(ruta)


def procesar_correos(data: dict, config: dict, mailbox_dir: Path) -> list[dict]:
    correos = data["correos"]
    validar_correos(correos, config)
    resultados = []
    for correo in correos:
        categoria = detectar_categoria(correo, config["reglas_clasificacion"])
        prioridad = detectar_prioridad(correo)
        requiere_respuesta = bool(correo["requiere_respuesta"])
        requiere_tarea = detectar_requiere_tarea(correo, config)
        sensibilidad = detectar_sensibilidad(correo, config["reglas_sensibilidad"])
        respuesta = generar_respuesta(correo, categoria, prioridad, config)
        tarea = generar_tarea(correo, requiere_tarea)
        accion = "archivar"
        if requiere_respuesta and requiere_tarea:
            accion = "responder_y_planificar"
        elif requiere_respuesta:
            accion = "responder"
        elif requiere_tarea:
            accion = "planificar"
        item = {
            "id_correo": correo["id_correo"],
            "categoria_detectada": categoria,
            "prioridad_detectada": prioridad,
            "requiere_respuesta": requiere_respuesta,
            "requiere_tarea": requiere_tarea,
            "respuesta_sugerida_simulada": respuesta,
            "tarea_sugerida_simulada": tarea,
            "sensibilidad_detectada": sensibilidad,
            "accion_recomendada": accion,
            "registro_generado": "",
            "usa_gmail_real": False,
            "usa_oauth_real": False,
            "usa_api_externa": False,
            "usa_cloud": False,
            "usa_ia_real": False,
        }
        item["registro_generado"] = generar_registro(mailbox_dir, item)
        resultados.append(item)
    return resultados


def generar_informe_markdown(resultado: dict, salida: Path) -> None:
    lineas = [
        "# Informe de Simulación Gmail IA Empresarial (Local)",
        "",
        f"**Fecha de generación:** {resultado['fecha_generacion']}",
        "",
        "## Resumen ejecutivo",
        "Flujo de correos empresariales sintéticos procesado sin Gmail real, OAuth real, API externa, cloud ni IA real.",
        "",
        "## Total de correos simulados",
        f"- {resultado['total_correos']}",
        "",
        "## Distribución por categoría",
    ]
    for k, v in resultado["distribucion_categoria"].items():
        lineas.append(f"- {k}: {v}")
    lineas.extend(["", "## Distribución por prioridad"])
    for k, v in resultado["distribucion_prioridad"].items():
        lineas.append(f"- {k}: {v}")
    lineas.extend(["", "## Correos que requieren respuesta", f"- {resultado['requieren_respuesta']}", "", "## Correos que requieren tarea", f"- {resultado['requieren_tarea']}", "", "## Sensibilidad detectada"])
    for k, v in resultado["sensibilidad_detectada"].items():
        lineas.append(f"- {k}: {v}")
    lineas.extend(["", "## Ejemplos de respuestas simuladas"])
    for item in resultado["resultados"][:3]:
        lineas.append(f"- {item['id_correo']}: {item['respuesta_sugerida_simulada']}")
    lineas.extend(
        [
            "",
            "## Límites de la simulación",
            "Sin uso de Gmail real, Gmail API, OAuth real, Google Cloud, datos reales ni modelos LLM reales.",
            "",
            "## Recomendaciones siguientes",
            "1. Añadir reglas por sector de PYME en datasets sintéticos.",
            "2. Ampliar escenarios de sensibilidad y escalado operativo.",
            "3. Definir conector V2 opcional por `.env` con fallback local.",
            "",
            "## 🪪 Licencia y Autoría",
            "Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  ",
            "© 2025 – Txema Ríos. Todos los derechos compartidos.",
        ]
    )
    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.write_text("\n".join(lineas), encoding="utf-8")


def construir_resultado_global(resultados: list[dict], config: dict) -> dict:
    return {
        "fecha_generacion": datetime.now().isoformat(timespec="seconds"),
        "total_correos": len(resultados),
        "distribucion_categoria": dict(Counter(x["categoria_detectada"] for x in resultados)),
        "distribucion_prioridad": dict(Counter(x["prioridad_detectada"] for x in resultados)),
        "requieren_respuesta": sum(1 for x in resultados if x["requiere_respuesta"]),
        "requieren_tarea": sum(1 for x in resultados if x["requiere_tarea"]),
        "sensibilidad_detectada": dict(Counter(x["sensibilidad_detectada"] for x in resultados)),
        "nota": config.get("nota", ""),
        "resultados": resultados,
    }


def parsear_argumentos() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Simulador local de Gmail IA empresarial")
    parser.add_argument("--emails", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output-md", required=True)
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--mailbox-dir", required=True)
    return parser.parse_args()


def main() -> None:
    args = parsear_argumentos()
    data = cargar_json(Path(args.emails))
    config = cargar_json(Path(args.config))
    resultados = procesar_correos(data, config, Path(args.mailbox_dir))
    resumen = construir_resultado_global(resultados, config)
    out_json = Path(args.output_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(resumen, ensure_ascii=False, indent=2), encoding="utf-8")
    generar_informe_markdown(resumen, Path(args.output_md))


if __name__ == "__main__":
    main()
