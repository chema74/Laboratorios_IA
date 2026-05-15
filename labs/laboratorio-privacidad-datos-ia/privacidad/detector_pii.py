import re

PATRONES = {
    "email": re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"),
    "telefono": re.compile(r"\b(?:\+34\s?)?[6789]\d{8}\b"),
    "identificador": re.compile(r"\b[A-Z]{1}\d{8}[A-Z]\b"),
    "direccion": re.compile(r"\b(?:Calle|Avda\.|Avenida|Plaza)\s+[A-Za-z0-9\s]+\b"),
}


def detectar_pii(texto: str, nombres_marcados: list[str] | None = None) -> list[dict]:
    hallazgos = []
    t = texto or ""
    for tipo, patron in PATRONES.items():
        for m in patron.finditer(t):
            sev = "alta" if tipo in {"email", "identificador"} else "media"
            hallazgos.append({"tipo": tipo, "valor": m.group(0), "inicio": m.start(), "severidad": sev})

    if nombres_marcados:
        for n in nombres_marcados:
            idx = t.find(n)
            if idx >= 0:
                hallazgos.append({"tipo": "nombre", "valor": n, "inicio": idx, "severidad": "media"})

    hallazgos.sort(key=lambda x: x["inicio"])
    return hallazgos
