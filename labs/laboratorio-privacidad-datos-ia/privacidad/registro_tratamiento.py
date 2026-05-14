def resumir_tratamiento(registro: dict, medidas: list[str], evidencias: list[str]) -> dict:
    return {
        "finalidad": registro.get("finalidad", "orientativa"),
        "categorias_datos": registro.get("categorias_datos", []),
        "base_documental_ficticia": registro.get("base_documental_ficticia", "N/A"),
        "medidas_aplicadas": medidas,
        "retencion_sintetica": registro.get("retencion_sintetica", "N/A"),
        "evidencias_generadas": evidencias,
        "aviso": "Resumen técnico orientativo, sin valor legal definitivo.",
    }
