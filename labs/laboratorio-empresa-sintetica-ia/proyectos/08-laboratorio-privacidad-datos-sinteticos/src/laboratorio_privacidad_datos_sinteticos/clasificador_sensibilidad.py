"""Inventario y clasificación de sensibilidad ficticia."""

from __future__ import annotations

from collections import Counter

from .modelos import InventarioDato, dataclass_a_dict

NIVELES_SENSIBILIDAD = ["publica", "interna", "confidencial", "critica"]


def _resumir(valor: object, max_len: int = 40) -> str:
    texto = str(valor)
    return texto[:max_len] + ("..." if len(texto) > max_len else "")


def _clasificar_campo(campo: str) -> tuple[str, str, bool, bool, bool]:
    campo_l = campo.lower()
    if "id_" in campo_l:
        return ("confidencial", "identificador_ficticio", True, True, True)
    if "nombre" in campo_l:
        return ("interna", "identidad_ficticia", True, True, False)
    if any(x in campo_l for x in ["riesgo", "severidad", "crisis", "privacidad"]):
        return ("critica", "riesgo_operativo", True, False, True)
    if any(x in campo_l for x in ["descripcion", "decision", "estado"]):
        return ("interna", "operativo", False, False, False)
    return ("publica", "general", False, False, False)


def _extraer_registros(origen: str, tipo_entidad: str, objetos: list[dict]) -> list[tuple[str, str, str, object]]:
    filas: list[tuple[str, str, str, object]] = []
    for obj in objetos:
        for campo, valor in obj.items():
            filas.append((origen, tipo_entidad, campo, valor))
    return filas


def construir_inventario_datos(contexto: dict, max_datos: int = 80) -> list[dict]:
    """
    1) Extrae campos desde múltiples orígenes sintéticos.
    2) Clasifica sensibilidad ficticia por reglas simples.
    3) Devuelve inventario normalizado y limitado por `max_datos`.
    """
    colecciones: list[tuple[str, str, list[dict]]] = []

    empresa = contexto.get("empresa", {})
    colecciones.append(("empresa", "empresa", [empresa.get("empresa", {})]))
    colecciones.append(("empresa", "cliente", empresa.get("clientes", [])))
    colecciones.append(("empresa", "empleado", empresa.get("empleados", [])))
    colecciones.append(("eventos", "evento", contexto.get("eventos", [])))
    colecciones.append(("documentos", "documento", contexto.get("documentos", [])))
    colecciones.append(("escenarios", "escenario", contexto.get("escenarios", [])))
    colecciones.append(("crisis", "crisis", contexto.get("crisis", [])))
    colecciones.append(("revisiones", "revision", contexto.get("revisiones", [])))
    colecciones.append(("registro_decisiones", "registro_decision", contexto.get("registro_decisiones", [])))
    colecciones.append(("estado_operativo", "estado_operativo", [contexto.get("estado_operativo", {})]))
    colecciones.append(("alertas_operativas", "alerta", contexto.get("alertas_operativas", [])))
    colecciones.append(("decisiones_simuladas", "decision", contexto.get("decisiones_simuladas", [])))

    inventario: list[dict] = []
    idx = 1

    for origen, tipo_entidad, objetos in colecciones:
        registros = _extraer_registros(origen, tipo_entidad, [o for o in objetos if isinstance(o, dict)])
        for _, _, campo, valor in registros:
            nivel, categoria, req_min, req_anon, req_rev = _clasificar_campo(campo)
            item = InventarioDato(
                id_dato=f"DAT-{idx:06d}",
                origen=origen,
                tipo_entidad=tipo_entidad,
                campo=campo,
                valor_simulado_resumido=_resumir(valor),
                nivel_sensibilidad_ficticia=nivel,
                categoria_privacidad_simulada=categoria,
                uso_previsto="pruebas_ia_empresarial_simulada",
                requiere_minimizacion=req_min,
                requiere_anonimizacion=req_anon,
                requiere_revision_humana=req_rev,
                origen_simulado="laboratorio_privacidad_datos_sinteticos_v1_local",
            )
            inventario.append(dataclass_a_dict(item))
            idx += 1
            if len(inventario) >= max_datos:
                return inventario

    return inventario


def construir_clasificacion_sensibilidad(inventario: list[dict]) -> list[dict]:
    claves = Counter(
        (
            d["origen"],
            d["tipo_entidad"],
            d["nivel_sensibilidad_ficticia"],
            d["categoria_privacidad_simulada"],
            d["requiere_revision_humana"],
        )
        for d in inventario
    )
    salida = []
    for i, (k, total) in enumerate(claves.items(), start=1):
        salida.append(
            {
                "id_clasificacion": f"CLS-{i:05d}",
                "origen": k[0],
                "tipo_entidad": k[1],
                "nivel_sensibilidad_ficticia": k[2],
                "categoria_privacidad_simulada": k[3],
                "requiere_revision_humana": k[4],
                "total": total,
            }
        )
    return salida
