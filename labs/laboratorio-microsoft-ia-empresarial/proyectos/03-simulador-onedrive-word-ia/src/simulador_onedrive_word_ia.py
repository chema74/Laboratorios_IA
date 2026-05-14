import argparse
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

CAMPOS_OBLIGATORIOS = [
    "id_documento",
    "nombre_documento",
    "tipo_documento",
    "propietario_ficticio",
    "carpeta_onedrive_simulada",
    "contenido_sintetico",
    "fecha_simulada",
    "sensibilidad_simulada",
    "accion_ia_esperada",
    "resumen_esperado_simulado",
    "etiquetas_esperadas",
    "requiere_revision_humana",
    "permisos_simulados",
    "limites_declarados",
    "usa_onedrive_real",
    "usa_word_real",
    "usa_microsoft_graph_real",
    "usa_oauth_real",
    "usa_api_externa",
    "usa_azure",
    "usa_ia_real",
    "nota_sintetica",
]


def cargar_json(ruta: Path) -> dict:
    with ruta.open("r", encoding="utf-8") as f:
        return json.load(f)


def validar_documentos(documentos: list[dict], config: dict) -> None:
    tipos = set(config.get("tipos_documento_permitidos", []))
    carpetas = set(config.get("carpetas_onedrive_simuladas", []))
    acciones = set(config.get("acciones_ia_simuladas", []))
    sensibilidades = set(config.get("reglas_sensibilidad", []))
    permisos = set(config.get("permisos_simulados_permitidos", []))
    for i, doc in enumerate(documentos, start=1):
        faltantes = [c for c in CAMPOS_OBLIGATORIOS if c not in doc]
        if faltantes:
            raise ValueError(f"Documento {i} invalido: faltan {faltantes}")
        if doc["tipo_documento"] not in tipos:
            raise ValueError(f"Tipo no permitido: {doc['id_documento']}")
        if doc["carpeta_onedrive_simulada"] not in carpetas:
            raise ValueError(f"Carpeta no permitida: {doc['id_documento']}")
        if doc["accion_ia_esperada"] not in acciones:
            raise ValueError(f"Accion IA no permitida: {doc['id_documento']}")
        if doc["sensibilidad_simulada"] not in sensibilidades:
            raise ValueError(f"Sensibilidad no permitida: {doc['id_documento']}")
        if doc["permisos_simulados"] not in permisos:
            raise ValueError(f"Permiso no permitido: {doc['id_documento']}")
        for bandera in [
            "usa_onedrive_real",
            "usa_word_real",
            "usa_microsoft_graph_real",
            "usa_oauth_real",
            "usa_api_externa",
            "usa_azure",
            "usa_ia_real",
        ]:
            if doc[bandera] is not False:
                raise ValueError(f"{doc['id_documento']} incumple politica en {bandera}")


def resumir_contenido(texto: str, max_palabras: int) -> str:
    palabras = texto.split()
    if len(palabras) <= max_palabras:
        return " ".join(palabras)
    return " ".join(palabras[:max_palabras]) + "..."


def etiquetar_documento(doc: dict, max_etiquetas: int) -> list[str]:
    etiquetas = []
    etiquetas.extend(doc.get("etiquetas_esperadas", []))
    etiquetas.append(doc["tipo_documento"].split()[0].lower())
    base = []
    for e in etiquetas:
        if e not in base:
            base.append(e)
    return base[:max_etiquetas]


def generar_registro_documento(docs_dir: Path, resultado: dict) -> str:
    docs_dir.mkdir(parents=True, exist_ok=True)
    ruta = docs_dir / f"{resultado['id_documento']}.json"
    ruta.write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(ruta)


def generar_informe_md(resultados: list[dict]) -> str:
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total = len(resultados)
    por_tipo = Counter(r["tipo_documento_detectado"] for r in resultados)
    por_carpeta = Counter(r["carpeta_onedrive_simulada"] for r in resultados)
    por_sensibilidad = Counter(r["sensibilidad_detectada"] for r in resultados)
    por_accion = Counter(r["accion_ia_simulada"] for r in resultados)
    revisiones = [r["id_documento"] for r in resultados if r["requiere_revision_humana"]]
    md = [
        "# Informe Simulador OneDrive y Word IA (V1 Local)",
        "",
        f"Fecha de generación: {fecha}",
        "",
        "## Resumen ejecutivo",
        "Simulación local de flujos documentales OneDrive/Word con acciones IA simuladas y trazabilidad por documento.",
        "",
        "## Total de documentos simulados",
        f"- {total}",
        "",
        "## Distribución por tipo documental",
    ]
    for k in sorted(por_tipo):
        md.append(f"- {k}: {por_tipo[k]}")
    md.extend(["", "## Distribución por carpeta simulada"])
    for k in sorted(por_carpeta):
        md.append(f"- {k}: {por_carpeta[k]}")
    md.extend(["", "## Sensibilidad detectada"])
    for k in sorted(por_sensibilidad):
        md.append(f"- {k}: {por_sensibilidad[k]}")
    md.extend(["", "## Documentos que requieren revisión humana"])
    md.append("- " + ", ".join(revisiones) if revisiones else "- Ninguno")
    md.extend(["", "## Acciones IA simuladas"])
    for k in sorted(por_accion):
        md.append(f"- {k}: {por_accion[k]}")
    md.extend(["", "## Ejemplos de resúmenes simulados"])
    for r in resultados[:3]:
        md.append(f"- {r['id_documento']}: {r['resumen_simulado']}")
    md.extend(
        [
            "",
            "## Límites de la simulación",
            "- Sin OneDrive real.",
            "- Sin Word real.",
            "- Sin Microsoft Graph API real.",
            "- Sin OAuth real.",
            "- Sin Azure obligatorio.",
            "- Sin IA real ni datos reales.",
            "",
            "## Recomendaciones siguientes",
            "- Mantener reglas de revisión humana por sensibilidad.",
            "- Versionar criterios de etiquetado por tipo de documento.",
            "- Diseñar integración V2 opcional mediante .env con fallback local.",
            "",
            "## 🪪 Licencia y Autoría",
            "Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  ",
            "© 2025 – Txema Ríos. Todos los derechos compartidos.",
            "",
        ]
    )
    return "\n".join(md)


def ejecutar(documents_path: Path, config_path: Path, output_md: Path, output_json: Path, docs_dir: Path) -> dict:
    data = cargar_json(documents_path)
    config = cargar_json(config_path)
    documentos = data.get("documentos", [])
    if not documentos:
        raise ValueError("No hay documentos para procesar.")
    validar_documentos(documentos, config)

    max_palabras = int(config["reglas_resumen"]["max_palabras"])
    max_etiquetas = int(config["reglas_etiquetado"]["max_etiquetas"])
    revisar_por_sensibilidad = set(config.get("reglas_revision_humana", []))
    resultados = []
    for doc in documentos:
        resumen = resumir_contenido(doc["contenido_sintetico"], max_palabras)
        etiquetas = etiquetar_documento(doc, max_etiquetas)
        requiere_revision = doc["requiere_revision_humana"] or doc["sensibilidad_simulada"] in revisar_por_sensibilidad
        resultado = {
            "id_documento": doc["id_documento"],
            "nombre_documento": doc["nombre_documento"],
            "tipo_documento_detectado": doc["tipo_documento"],
            "carpeta_onedrive_simulada": doc["carpeta_onedrive_simulada"],
            "resumen_simulado": resumen,
            "etiquetas_simuladas": etiquetas,
            "sensibilidad_detectada": doc["sensibilidad_simulada"],
            "requiere_revision_humana": bool(requiere_revision),
            "permisos_simulados": doc["permisos_simulados"],
            "accion_ia_simulada": doc["accion_ia_esperada"],
            "registro_generado": "",
            "usa_onedrive_real": False,
            "usa_word_real": False,
            "usa_microsoft_graph_real": False,
            "usa_oauth_real": False,
            "usa_api_externa": False,
            "usa_azure": False,
            "usa_ia_real": False,
        }
        resultado["registro_generado"] = generar_registro_documento(docs_dir, resultado)
        resultados.append(resultado)

    salida = {
        "metadata": {
            "fecha_generacion": datetime.now().isoformat(timespec="seconds"),
            "total_documentos": len(resultados),
            "nota": config.get("nota", ""),
        },
        "resumen_por_tipo_documental": dict(Counter(r["tipo_documento_detectado"] for r in resultados)),
        "resumen_por_carpeta": dict(Counter(r["carpeta_onedrive_simulada"] for r in resultados)),
        "resumen_por_sensibilidad": dict(Counter(r["sensibilidad_detectada"] for r in resultados)),
        "resumen_por_accion_ia_simulada": dict(Counter(r["accion_ia_simulada"] for r in resultados)),
        "resultados": resultados,
    }

    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(generar_informe_md(resultados), encoding="utf-8")
    output_json.write_text(json.dumps(salida, ensure_ascii=False, indent=2), encoding="utf-8")
    return salida


def crear_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Simulador local de OneDrive y Word con IA simulada.")
    parser.add_argument("--documents", required=True, type=Path)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--output-md", required=True, type=Path)
    parser.add_argument("--output-json", required=True, type=Path)
    parser.add_argument("--docs-dir", required=True, type=Path)
    return parser


def main() -> None:
    args = crear_parser().parse_args()
    ejecutar(args.documents, args.config, args.output_md, args.output_json, args.docs_dir)


if __name__ == "__main__":
    main()
