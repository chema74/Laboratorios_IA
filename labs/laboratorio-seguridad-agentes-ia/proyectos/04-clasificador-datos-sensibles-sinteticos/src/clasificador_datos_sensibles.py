from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any


def cargar_json(ruta: Path) -> Any:
    with ruta.open("r", encoding="utf-8") as f:
        return json.load(f)


def validar_estructura_registro(registro: dict[str, Any]) -> list[str]:
    campos = [
        "id_registro",
        "texto_sintetico",
        "campos_detectables",
        "contexto_simulado",
        "sensibilidad_esperada",
        "accion_defensiva_esperada",
        "requiere_minimizacion",
        "requiere_enmascarado",
        "requiere_revision_humana",
        "limites_declarados",
        "usa_datos_reales",
        "usa_ia_real",
        "usa_api_externa",
        "usa_cloud",
        "nota_sintetica",
    ]
    return [f"Falta campo obligatorio: {c}" for c in campos if c not in registro]


def detectar_sensibilidad(texto: str, config: dict[str, Any]) -> str:
    for tipo, patrones in config["patrones_defensivos_sinteticos"].items():
        if any(p in texto for p in patrones):
            return tipo
    return "interno ficticio"


def enmascarar_texto(texto: str) -> str:
    return re.sub(r"\[[A-Z_]+\]", "[DATO_ENMASCARADO]", texto)


def clasificar_registro(registro: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    sensibilidad = detectar_sensibilidad(registro["texto_sintetico"], config)
    accion = config["acciones_defensivas"].get(sensibilidad, "revisar")
    severidad = config["severidades"].get(sensibilidad, "media")
    minimizacion = sensibilidad in config["reglas_minimizacion"]
    enmascarado = sensibilidad in config["reglas_enmascarado"]
    revision = accion.endswith("revisar") or "revisar" in accion

    salida = dict(registro)
    salida["sensibilidad_detectada"] = sensibilidad
    salida["severidad_simulada"] = severidad
    salida["accion_defensiva_recomendada"] = accion
    salida["marcar_minimizacion"] = minimizacion
    salida["marcar_enmascarado"] = enmascarado
    salida["marcar_revision_humana"] = revision or registro.get("requiere_revision_humana", False)
    salida["texto_enmascarado_simulado"] = enmascarar_texto(registro["texto_sintetico"])
    return salida


def ejecutar_clasificacion(datos: list[dict[str, Any]], config: dict[str, Any]) -> dict[str, Any]:
    errores: list[str] = []
    resultados: list[dict[str, Any]] = []
    for registro in datos:
        err = validar_estructura_registro(registro)
        if registro.get("sensibilidad_esperada") not in config["tipos_sensibilidad"]:
            err.append("sensibilidad_esperada no permitida")
        for bandera in ("usa_datos_reales", "usa_ia_real", "usa_api_externa", "usa_cloud"):
            if registro.get(bandera) is not False:
                err.append(f"{bandera} debe ser false")
        if not re.search(r"\[[A-Z_]+\]", registro.get("texto_sintetico", "")):
            err.append("texto_sintetico debe usar placeholders ficticios")
        if err:
            errores.append(f"{registro.get('id_registro', 'SIN_ID')}: " + " | ".join(err))
            continue
        resultados.append(clasificar_registro(registro, config))

    return {
        "fecha_generacion": datetime.now().isoformat(timespec="seconds"),
        "total_registros_analizados": len(resultados),
        "errores_validacion": errores,
        "distribucion_por_sensibilidad": dict(Counter(r["sensibilidad_detectada"] for r in resultados)),
        "distribucion_por_accion_defensiva": dict(Counter(r["accion_defensiva_recomendada"] for r in resultados)),
        "registros_minimizacion": [r for r in resultados if r["marcar_minimizacion"]],
        "registros_enmascarado": [r for r in resultados if r["marcar_enmascarado"]],
        "registros_revision_humana": [r for r in resultados if r["marcar_revision_humana"]],
        "resultados": resultados,
    }


def generar_markdown(resultado: dict[str, Any]) -> str:
    lineas = [
        "# Informe de Clasificación de Sensibilidad de Datos Sintéticos",
        "",
        f"Fecha de generación: {resultado['fecha_generacion']}",
        "",
        "## Resumen ejecutivo",
        "Clasificación local de sensibilidad en registros sintéticos para aplicar minimización, enmascarado y revisión defensiva.",
        "",
        "## Total de registros analizados",
        str(resultado["total_registros_analizados"]),
        "",
        "## Distribución por sensibilidad",
    ]
    lineas.extend([f"- {k}: {v}" for k, v in resultado["distribucion_por_sensibilidad"].items()])
    lineas += ["", "## Registros que requieren minimización"]
    lineas.extend([f"- {r['id_registro']} - {r['sensibilidad_detectada']}" for r in resultado["registros_minimizacion"]] or ["- Ninguno"])
    lineas += ["", "## Registros que requieren enmascarado"]
    lineas.extend([f"- {r['id_registro']} - {r['sensibilidad_detectada']}" for r in resultado["registros_enmascarado"]] or ["- Ninguno"])
    lineas += ["", "## Registros que requieren revisión humana"]
    lineas.extend([f"- {r['id_registro']} - {r['sensibilidad_detectada']}" for r in resultado["registros_revision_humana"]] or ["- Ninguno"])
    lineas += ["", "## Acciones defensivas recomendadas"]
    lineas.extend([f"- {k}: {v}" for k, v in resultado["distribucion_por_accion_defensiva"].items()])
    lineas += [
        "",
        "## Lectura técnica defensiva",
        "Los marcadores de secreto o credencial ficticia elevan criticidad y activan bloqueo con revisión humana.",
        "",
        "## Límites del clasificador",
        "Reglas simples por placeholders sintéticos; no aplica a datos reales ni operación productiva.",
        "",
        "## Recomendaciones siguientes",
        "1. Ajustar reglas por contexto de negocio sintético.",
        "2. Integrar salida con políticas del proyecto 06.",
        "3. Cruzar hallazgos con informe defensivo del proyecto 09.",
        "",
        "## 🪪 Licencia y Autoría",
        "Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  ",
        "© 2025 – Txema Ríos. Todos los derechos compartidos.",
    ]
    return "\n".join(lineas) + "\n"


def ejecutar(ruta_data: Path, ruta_config: Path, salida_md: Path, salida_json: Path) -> dict[str, Any]:
    datos = cargar_json(ruta_data)
    config = cargar_json(ruta_config)
    if not isinstance(datos, list):
        raise ValueError("data debe ser lista")
    if not isinstance(config, dict):
        raise ValueError("config debe ser objeto")
    resultado = ejecutar_clasificacion(datos, config)
    salida_md.parent.mkdir(parents=True, exist_ok=True)
    salida_json.parent.mkdir(parents=True, exist_ok=True)
    salida_md.write_text(generar_markdown(resultado), encoding="utf-8")
    salida_json.write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8")
    return resultado


def main() -> None:
    parser = argparse.ArgumentParser(description="Clasificador local de sensibilidad de datos sintéticos.")
    parser.add_argument("--data", required=True, type=Path)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--output-md", required=True, type=Path)
    parser.add_argument("--output-json", required=True, type=Path)
    args = parser.parse_args()
    resultado = ejecutar(args.data, args.config, args.output_md, args.output_json)
    print(f"Clasificación completada. Registros válidos: {resultado['total_registros_analizados']}")


if __name__ == "__main__":
    main()
