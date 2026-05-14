"""Simulador local de Drive/Docs empresarial con IA simulada."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

CAMPOS_DOC = {
    "id_documento",
    "nombre_documento",
    "tipo_documento",
    "propietario_ficticio",
    "carpeta_simulada",
    "contenido_sintetico",
    "fecha_simulada",
    "sensibilidad_simulada",
    "accion_ia_esperada",
    "resumen_esperado_simulado",
    "etiquetas_esperadas",
    "requiere_revision_humana",
    "permisos_simulados",
    "limites_declarados",
    "usa_drive_real",
    "usa_docs_real",
    "usa_oauth_real",
    "usa_api_externa",
    "usa_cloud",
    "usa_ia_real",
    "nota_sintetica",
}


def cargar_json(ruta: Path) -> dict:
    with ruta.open("r", encoding="utf-8-sig") as archivo:
        return json.load(archivo)


def validar_documentos(documentos: list[dict], config: dict) -> None:
    tipos = set(config["tipos_documento_permitidos"])
    carpetas = set(config["carpetas_simuladas"])
    permisos = set(config["permisos_simulados_permitidos"])
    for doc in documentos:
        faltantes = CAMPOS_DOC.difference(doc.keys())
        if faltantes:
            raise ValueError(f"Documento incompleto {doc.get('id_documento')}: {sorted(faltantes)}")
        if doc["tipo_documento"] not in tipos:
            raise ValueError(f"Tipo no permitido: {doc['tipo_documento']}")
        if doc["carpeta_simulada"] not in carpetas:
            raise ValueError(f"Carpeta no permitida: {doc['carpeta_simulada']}")
        if doc["permisos_simulados"] not in permisos:
            raise ValueError(f"Permiso no permitido: {doc['permisos_simulados']}")


def generar_resumen_simulado(doc: dict, max_palabras: int) -> str:
    palabras = doc["contenido_sintetico"].split()
    return " ".join(palabras[:max_palabras])


def generar_etiquetas_simuladas(doc: dict, config: dict) -> list[str]:
    etiquetas = set(doc["etiquetas_esperadas"])
    texto = f"{doc['nombre_documento']} {doc['contenido_sintetico']}".lower()
    for palabra in config["reglas_etiquetado"]["palabras_clave"]:
        if palabra.lower() in texto:
            etiquetas.add(palabra.lower())
    return sorted(etiquetas)


def detectar_sensibilidad(doc: dict, config: dict) -> str:
    texto = f"{doc['nombre_documento']} {doc['contenido_sintetico']}".lower()
    for nivel, claves in config["reglas_sensibilidad"].items():
        if any(clave.lower() in texto for clave in claves):
            return nivel
    return doc["sensibilidad_simulada"]


def detectar_revision_humana(doc: dict, config: dict, sensibilidad: str) -> bool:
    return (
        doc["requiere_revision_humana"]
        or doc["tipo_documento"] in config["reglas_revision_humana"]["tipos_criticos"]
        or sensibilidad == "alta"
    )


def guardar_registro(docs_dir: Path, registro: dict) -> str:
    docs_dir.mkdir(parents=True, exist_ok=True)
    ruta = docs_dir / f"{registro['id_documento']}.json"
    ruta.write_text(json.dumps(registro, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(ruta)


def procesar_documentos(data: dict, config: dict, docs_dir: Path) -> list[dict]:
    documentos = data["documentos"]
    validar_documentos(documentos, config)
    resultados: list[dict] = []
    for doc in documentos:
        sensibilidad = detectar_sensibilidad(doc, config)
        requiere_revision = detectar_revision_humana(doc, config, sensibilidad)
        resumen = generar_resumen_simulado(doc, config["reglas_resumen"]["max_palabras"])
        etiquetas = generar_etiquetas_simuladas(doc, config)
        item = {
            "id_documento": doc["id_documento"],
            "nombre_documento": doc["nombre_documento"],
            "tipo_documento_detectado": doc["tipo_documento"],
            "carpeta_simulada": doc["carpeta_simulada"],
            "resumen_simulado": resumen,
            "etiquetas_simuladas": etiquetas,
            "sensibilidad_detectada": sensibilidad,
            "requiere_revision_humana": requiere_revision,
            "permisos_simulados": doc["permisos_simulados"],
            "accion_ia_simulada": doc["accion_ia_esperada"],
            "registro_generado": "",
            "usa_drive_real": False,
            "usa_docs_real": False,
            "usa_oauth_real": False,
            "usa_api_externa": False,
            "usa_cloud": False,
            "usa_ia_real": False,
        }
        item["registro_generado"] = guardar_registro(docs_dir, item)
        resultados.append(item)
    return resultados


def construir_resultado_global(resultados: list[dict], config: dict) -> dict:
    return {
        "fecha_generacion": datetime.now().isoformat(timespec="seconds"),
        "total_documentos": len(resultados),
        "distribucion_por_tipo": dict(Counter(x["tipo_documento_detectado"] for x in resultados)),
        "distribucion_por_carpeta": dict(Counter(x["carpeta_simulada"] for x in resultados)),
        "distribucion_sensibilidad": dict(Counter(x["sensibilidad_detectada"] for x in resultados)),
        "distribucion_accion_ia": dict(Counter(x["accion_ia_simulada"] for x in resultados)),
        "documentos_revision_humana": [x["id_documento"] for x in resultados if x["requiere_revision_humana"]],
        "nota": config["nota"],
        "resultados": resultados,
    }


def generar_informe_markdown(resultado: dict, output_md: Path) -> None:
    lineas = [
        "# Informe de Simulación Drive/Docs IA (Local)",
        "",
        f"**Fecha de generación:** {resultado['fecha_generacion']}",
        "",
        "## Resumen ejecutivo",
        "Documentos empresariales sintéticos procesados localmente sin Drive real, Docs real, OAuth real, APIs externas ni IA real.",
        "",
        "## Total de documentos simulados",
        f"- {resultado['total_documentos']}",
        "",
        "## Distribución por tipo documental",
    ]
    for k, v in resultado["distribucion_por_tipo"].items():
        lineas.append(f"- {k}: {v}")
    lineas.extend(["", "## Distribución por carpeta simulada"])
    for k, v in resultado["distribucion_por_carpeta"].items():
        lineas.append(f"- {k}: {v}")
    lineas.extend(["", "## Sensibilidad detectada"])
    for k, v in resultado["distribucion_sensibilidad"].items():
        lineas.append(f"- {k}: {v}")
    lineas.extend(["", "## Documentos que requieren revisión humana"])
    for doc_id in resultado["documentos_revision_humana"]:
        lineas.append(f"- {doc_id}")
    lineas.extend(["", "## Acciones IA simuladas"])
    for k, v in resultado["distribucion_accion_ia"].items():
        lineas.append(f"- {k}: {v}")
    lineas.extend(["", "## Ejemplos de resúmenes simulados"])
    for item in resultado["resultados"][:3]:
        lineas.append(f"- {item['id_documento']}: {item['resumen_simulado']}")
    lineas.extend(
        [
            "",
            "## Límites de la simulación",
            "Sin uso de Drive real, Docs real, OAuth real, APIs reales, Google Cloud ni IA real.",
            "",
            "## Recomendaciones siguientes",
            "1. Aumentar reglas de etiquetado por área.",
            "2. Integrar trazabilidad cruzada con los módulos 01 y 02.",
            "3. Definir interfaz V2 opcional por `.env` con fallback local.",
            "",
            "## 🪪 Licencia y Autoría",
            "Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  ",
            "© 2025 – Txema Ríos. Todos los derechos compartidos.",
        ]
    )
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text("\n".join(lineas), encoding="utf-8")


def parsear_argumentos() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Simulador local de Drive/Docs con IA simulada")
    parser.add_argument("--documents", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output-md", required=True)
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--docs-dir", required=True)
    return parser.parse_args()


def main() -> None:
    args = parsear_argumentos()
    data = cargar_json(Path(args.documents))
    config = cargar_json(Path(args.config))
    resultados = procesar_documentos(data, config, Path(args.docs_dir))
    resumen = construir_resultado_global(resultados, config)
    out_json = Path(args.output_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(resumen, ensure_ascii=False, indent=2), encoding="utf-8")
    generar_informe_markdown(resumen, Path(args.output_md))


if __name__ == "__main__":
    main()
