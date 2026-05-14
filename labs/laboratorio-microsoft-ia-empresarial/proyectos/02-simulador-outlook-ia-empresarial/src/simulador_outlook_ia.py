import argparse
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

CAMPOS_CORREO_OBLIGATORIOS = [
    "id_correo",
    "remitente_ficticio",
    "destinatario_ficticio",
    "asunto",
    "cuerpo_sintetico",
    "fecha_simulada",
    "carpeta_simulada",
    "categoria_esperada",
    "prioridad_esperada",
    "requiere_respuesta",
    "requiere_tarea",
    "requiere_reunion",
    "sensibilidad_simulada",
    "accion_recomendada_esperada",
    "limites_declarados",
    "usa_outlook_real",
    "usa_microsoft_graph_real",
    "usa_oauth_real",
    "usa_api_externa",
    "usa_azure",
    "usa_ia_real",
    "nota_sintetica",
]


def cargar_json(ruta: Path) -> dict:
    with ruta.open("r", encoding="utf-8") as archivo:
        return json.load(archivo)


def validar_correos(correos: list[dict], config: dict) -> None:
    categorias = set(config.get("categorias_permitidas", []))
    prioridades = set(config.get("prioridades_permitidas", []))
    sensibilidades = set(config.get("reglas_sensibilidad", []))

    for i, correo in enumerate(correos, start=1):
        faltantes = [campo for campo in CAMPOS_CORREO_OBLIGATORIOS if campo not in correo]
        if faltantes:
            raise ValueError(f"Correo {i} invalido. Faltan campos: {faltantes}")
        if correo["categoria_esperada"] not in categorias:
            raise ValueError(f"Categoria esperada no permitida: {correo['id_correo']}")
        if correo["prioridad_esperada"] not in prioridades:
            raise ValueError(f"Prioridad esperada no permitida: {correo['id_correo']}")
        if correo["sensibilidad_simulada"] not in sensibilidades:
            raise ValueError(f"Sensibilidad no permitida: {correo['id_correo']}")

        for bandera in [
            "usa_outlook_real",
            "usa_microsoft_graph_real",
            "usa_oauth_real",
            "usa_api_externa",
            "usa_azure",
            "usa_ia_real",
        ]:
            if correo[bandera] is not False:
                raise ValueError(f"{correo['id_correo']} incumple politica en {bandera}")


def clasificar_categoria(correo: dict, reglas_clasificacion: dict) -> str:
    texto = f"{correo['asunto']} {correo['cuerpo_sintetico']}".lower()
    for categoria, keywords in reglas_clasificacion.items():
        if any(keyword.lower() in texto for keyword in keywords):
            return categoria
    return correo["categoria_esperada"]


def detectar_prioridad(correo: dict) -> str:
    if correo["requiere_reunion"] and correo["requiere_tarea"]:
        return "alta"
    if correo["requiere_respuesta"] or correo["requiere_tarea"]:
        return "media"
    return correo["prioridad_esperada"]


def detectar_carpeta(categoria: str, requiere_reunion: bool, requiere_tarea: bool) -> str:
    if requiere_reunion:
        return "Reuniones"
    if requiere_tarea:
        return "Seguimiento"
    if categoria == "informativo":
        return "Archivado"
    return "Entrada"


def respuesta_simulada(prioridad: str, reglas: dict) -> str:
    base = reglas.get(prioridad, "Respuesta simulada estandar.")
    return f"{base} Mensaje generado localmente sin IA real."


def tarea_simulada(correo: dict, prioridad: str, reglas: dict) -> str:
    if not correo["requiere_tarea"]:
        return "No aplica"
    return f"{reglas.get(prioridad, 'Crear tarea local.')}: {correo['asunto']}"


def reunion_simulada(correo: dict, prioridad: str, reglas: dict) -> str:
    if not correo["requiere_reunion"]:
        return "No aplica"
    return f"{reglas.get(prioridad, 'Programar reunion local.')} Tema: {correo['asunto']}"


def guardar_registro_correo(mailbox_dir: Path, resultado: dict) -> str:
    mailbox_dir.mkdir(parents=True, exist_ok=True)
    ruta = mailbox_dir / f"{resultado['id_correo']}.json"
    ruta.write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(ruta)


def generar_informe_md(resultados: list[dict]) -> str:
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total = len(resultados)
    por_carpeta = Counter(r["carpeta_detectada"] for r in resultados)
    por_categoria = Counter(r["categoria_detectada"] for r in resultados)
    por_prioridad = Counter(r["prioridad_detectada"] for r in resultados)
    con_respuesta = [r["id_correo"] for r in resultados if r["requiere_respuesta"]]
    con_tarea = [r["id_correo"] for r in resultados if r["requiere_tarea"]]
    con_reunion = [r["id_correo"] for r in resultados if r["requiere_reunion"]]
    sensibilidad = Counter(r["sensibilidad_detectada"] for r in resultados)

    md = []
    md.append("# Informe de Simulador Outlook IA Empresarial (V1 Local)")
    md.append("")
    md.append(f"Fecha de generacion: {fecha}")
    md.append("")
    md.append("## Resumen ejecutivo")
    md.append("Simulacion local de bandeja Outlook empresarial con clasificacion, priorizacion y sugerencias sinteticas sin Outlook real ni IA real.")
    md.append("")
    md.append("## Total de correos simulados")
    md.append(f"- {total}")
    md.append("")
    md.append("## Distribucion por carpeta")
    for k in sorted(por_carpeta):
        md.append(f"- {k}: {por_carpeta[k]}")
    md.append("")
    md.append("## Distribucion por categoria")
    for k in sorted(por_categoria):
        md.append(f"- {k}: {por_categoria[k]}")
    md.append("")
    md.append("## Distribucion por prioridad")
    for k in sorted(por_prioridad):
        md.append(f"- {k}: {por_prioridad[k]}")
    md.append("")
    md.append("## Correos que requieren respuesta")
    md.append("- " + ", ".join(con_respuesta) if con_respuesta else "- Ninguno")
    md.append("")
    md.append("## Correos que requieren tarea")
    md.append("- " + ", ".join(con_tarea) if con_tarea else "- Ninguno")
    md.append("")
    md.append("## Correos que requieren reunion")
    md.append("- " + ", ".join(con_reunion) if con_reunion else "- Ninguno")
    md.append("")
    md.append("## Sensibilidad detectada")
    for k in sorted(sensibilidad):
        md.append(f"- {k}: {sensibilidad[k]}")
    md.append("")
    md.append("## Ejemplos de respuestas simuladas")
    for r in resultados[:3]:
        md.append(f"- {r['id_correo']}: {r['respuesta_sugerida_simulada']}")
    md.append("")
    md.append("## Limites de la simulacion")
    md.append("- Sin Outlook real.")
    md.append("- Sin Microsoft Graph API real.")
    md.append("- Sin OAuth real.")
    md.append("- Sin Azure obligatorio.")
    md.append("- Sin IA real ni datos reales.")
    md.append("")
    md.append("## Recomendaciones siguientes")
    md.append("- Mantener datos sinteticos y trazabilidad por correo.")
    md.append("- Versionar reglas de clasificacion para comparar resultados.")
    md.append("- Preparar interfaz opcional V2 con .env y fallback local.")
    md.append("")
    md.append("## 🪪 Licencia y Autoría")
    md.append("Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  ")
    md.append("© 2025 – Txema Ríos. Todos los derechos compartidos.")
    return "\n".join(md) + "\n"


def ejecutar(emails_path: Path, config_path: Path, output_md: Path, output_json: Path, mailbox_dir: Path) -> dict:
    data = cargar_json(emails_path)
    config = cargar_json(config_path)
    correos = data.get("correos", [])
    if not correos:
        raise ValueError("No hay correos sinteticos disponibles.")

    validar_correos(correos, config)
    resultados = []
    for correo in correos:
        categoria = clasificar_categoria(correo, config["reglas_clasificacion"])
        prioridad = detectar_prioridad(correo)
        carpeta = detectar_carpeta(categoria, correo["requiere_reunion"], correo["requiere_tarea"])
        respuesta = respuesta_simulada(prioridad, config["reglas_respuesta_simulada"])
        tarea = tarea_simulada(correo, prioridad, config["reglas_tarea_simulada"])
        reunion = reunion_simulada(correo, prioridad, config["reglas_reunion_simulada"])

        resultado = {
            "id_correo": correo["id_correo"],
            "carpeta_detectada": carpeta,
            "categoria_detectada": categoria,
            "prioridad_detectada": prioridad,
            "requiere_respuesta": correo["requiere_respuesta"],
            "requiere_tarea": correo["requiere_tarea"],
            "requiere_reunion": correo["requiere_reunion"],
            "respuesta_sugerida_simulada": respuesta,
            "tarea_sugerida_simulada": tarea,
            "reunion_sugerida_simulada": reunion,
            "sensibilidad_detectada": correo["sensibilidad_simulada"],
            "accion_recomendada": correo["accion_recomendada_esperada"],
            "registro_generado": "",
            "usa_outlook_real": False,
            "usa_microsoft_graph_real": False,
            "usa_oauth_real": False,
            "usa_api_externa": False,
            "usa_azure": False,
            "usa_ia_real": False,
        }
        resultado["registro_generado"] = guardar_registro_correo(mailbox_dir, resultado)
        resultados.append(resultado)

    salida = {
        "metadata": {
            "fecha_generacion": datetime.now().isoformat(timespec="seconds"),
            "total_correos": len(resultados),
            "nota": config.get("nota", ""),
        },
        "resumen_por_carpeta": dict(Counter(r["carpeta_detectada"] for r in resultados)),
        "resumen_por_categoria": dict(Counter(r["categoria_detectada"] for r in resultados)),
        "resumen_por_prioridad": dict(Counter(r["prioridad_detectada"] for r in resultados)),
        "resultados": resultados,
    }

    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(generar_informe_md(resultados), encoding="utf-8")
    output_json.write_text(json.dumps(salida, ensure_ascii=False, indent=2), encoding="utf-8")
    return salida


def crear_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Simulador local de Outlook empresarial con IA simulada.")
    parser.add_argument("--emails", required=True, type=Path)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--output-md", required=True, type=Path)
    parser.add_argument("--output-json", required=True, type=Path)
    parser.add_argument("--mailbox-dir", required=True, type=Path)
    return parser


def main() -> None:
    args = crear_parser().parse_args()
    ejecutar(args.emails, args.config, args.output_md, args.output_json, args.mailbox_dir)


if __name__ == "__main__":
    main()
