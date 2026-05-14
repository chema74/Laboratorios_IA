from datetime import datetime


def nueva_traza(prefix: str = "TRZ") -> str:
    return f"{prefix}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"


def resumen_trazas(registros: list[dict]) -> dict:
    return {"total": len(registros), "ok": sum(1 for r in registros if r.get("estado") == "ok"), "error": sum(1 for r in registros if r.get("estado") != "ok")}
