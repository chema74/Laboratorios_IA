import json

from api.respuestas import construir_respuesta
from api.router_local import enrutar
from api.validacion_contratos import validar_peticion
from auditoria.registro_peticiones import registrar_peticion
from observabilidad.costes_simulados import estimar_coste
from seguridad.autenticacion_ficticia import autenticar
from seguridad.autorizacion_roles import autorizar
from seguridad.politicas_acceso import modulo_por_endpoint


def _load(path):
    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def ejecutar_peticion(peticion: dict, usuarios: list[dict], bitacora: list[dict]) -> dict:
    v = validar_peticion(peticion)
    if not v["valida"]:
        registrar_peticion(bitacora, {"traza_id": peticion.get("traza_id", "N/A"), "usuario": peticion.get("usuario", "N/A"), "rol": peticion.get("rol", "N/A"), "endpoint": peticion.get("endpoint", "N/A"), "modulo": "N/A", "estado": "error", "resultado": "contrato_invalido"})
        return construir_respuesta("error", "CONTRATO_INVALIDO", "Petición incompleta", {"errores": v["errores"]}, {"traza_id": peticion.get("traza_id", "N/A")})

    auth = autenticar(peticion["usuario"], peticion.get("token_ficticio", ""), usuarios)
    if not auth["ok"]:
        registrar_peticion(bitacora, {"traza_id": peticion["traza_id"], "usuario": peticion["usuario"], "rol": peticion["rol"], "endpoint": peticion["endpoint"], "modulo": "N/A", "estado": "error", "resultado": "auth_fallida"})
        return construir_respuesta("error", "AUTH_FALLIDA", auth["motivo"], {}, {"traza_id": peticion["traza_id"]})

    modulo = modulo_por_endpoint(peticion["endpoint"])
    perm = autorizar(peticion["rol"], modulo)
    if not perm["ok"]:
        registrar_peticion(bitacora, {"traza_id": peticion["traza_id"], "usuario": peticion["usuario"], "rol": peticion["rol"], "endpoint": peticion["endpoint"], "modulo": modulo, "estado": "error", "resultado": "autorizacion_denegada"})
        return construir_respuesta("error", "NO_AUTORIZADO", perm["motivo"], {}, {"traza_id": peticion["traza_id"]})

    datos = enrutar(peticion["endpoint"], peticion["payload"])
    estado = "ok" if "error" not in datos else "error"
    registrar_peticion(bitacora, {"traza_id": peticion["traza_id"], "usuario": peticion["usuario"], "rol": peticion["rol"], "endpoint": peticion["endpoint"], "modulo": modulo, "estado": estado, "resultado": datos})
    return construir_respuesta(estado, "OK" if estado == "ok" else "ROUTER_ERROR", "Petición procesada", datos, {"traza_id": peticion["traza_id"]})


def ejecutar_lote(peticiones_path, usuarios_path) -> dict:
    peticiones = _load(peticiones_path)
    usuarios = _load(usuarios_path)
    bitacora = []
    respuestas = [ejecutar_peticion(p, usuarios, bitacora) for p in peticiones]
    coste = estimar_coste(len(peticiones))
    return {"respuestas": respuestas, "bitacora": bitacora, "coste": coste}
