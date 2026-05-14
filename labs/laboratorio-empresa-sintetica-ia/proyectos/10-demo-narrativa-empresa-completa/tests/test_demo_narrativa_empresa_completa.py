from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

RUTA_BASE = Path(__file__).resolve().parents[1]
RUTA_SRC = RUTA_BASE / "src"
if str(RUTA_SRC) not in sys.path:
    sys.path.insert(0, str(RUTA_SRC))

from demo_narrativa_empresa_completa.cli import crear_parser, ejecutar_desde_argumentos
from demo_narrativa_empresa_completa.constructor_narrativa import construir_demo_narrativa
from demo_narrativa_empresa_completa.linea_tiempo import SEVERIDADES


def _tmp(nombre: str) -> Path:
    base = RUTA_BASE / "tests" / ".tmp"
    base.mkdir(parents=True, exist_ok=True)
    p = base / nombre
    if p.exists():
        shutil.rmtree(p)
    p.mkdir(parents=True, exist_ok=True)
    return p


def _args_sin_entradas_existentes(salida: Path):
    parser = crear_parser()
    return parser.parse_args(
        [
            "--seed",
            "42",
            "--dias",
            "7",
            "--salida",
            str(salida),
            "--entrada-empresa",
            "no/existe/empresa.json",
            "--entrada-eventos",
            "no/existe/eventos.json",
            "--entrada-resumen-eventos",
            "no/existe/res_eventos.json",
            "--entrada-documentos",
            "no/existe/docs.json",
            "--entrada-resumen-documentos",
            "no/existe/res_docs.json",
            "--entrada-escenarios",
            "no/existe/escenarios.json",
            "--entrada-resumen-escenarios",
            "no/existe/res_escenarios.json",
            "--entrada-crisis",
            "no/existe/crisis.json",
            "--entrada-resumen-crisis",
            "no/existe/res_crisis.json",
            "--entrada-revisiones",
            "no/existe/revisiones.json",
            "--entrada-registro-decisiones",
            "no/existe/registro.json",
            "--entrada-resumen-revision",
            "no/existe/res_revision.json",
            "--entrada-estado-operativo",
            "no/existe/estado.json",
            "--entrada-alertas",
            "no/existe/alertas.json",
            "--entrada-decisiones",
            "no/existe/decisiones.json",
            "--entrada-resumen-gemelo",
            "no/existe/res_gemelo.json",
            "--entrada-inventario-privacidad",
            "no/existe/inventario.json",
            "--entrada-riesgos-privacidad",
            "no/existe/riesgos.json",
            "--entrada-resumen-privacidad",
            "no/existe/res_priv.json",
            "--entrada-procesos-comparados",
            "no/existe/procesos.json",
            "--entrada-comparaciones",
            "no/existe/comparaciones.json",
            "--entrada-resumen-comparador",
            "no/existe/res_comp.json",
        ]
    )


def test_estructura_narrativa_completa_y_reproducible():
    out = _tmp("demo_rep")
    args = _args_sin_entradas_existentes(out)
    narrativa_1, _ = ejecutar_desde_argumentos(args)
    narrativa_2, _ = ejecutar_desde_argumentos(args)

    claves = {
        "ficha_narrativa_empresa",
        "linea_tiempo_semanal",
        "episodios_narrativos",
        "mapa_evidencias",
        "resumen_ejecutivo_ficticio",
        "resumen_demo_narrativa",
    }
    assert claves.issubset(narrativa_1.keys())
    assert narrativa_1 == narrativa_2


def test_linea_tiempo_campos_obligatorios_y_severidad_controlada():
    out = _tmp("linea")
    narrativa, _ = ejecutar_desde_argumentos(_args_sin_entradas_existentes(out))
    hitos = narrativa["linea_tiempo_semanal"]
    assert hitos
    oblig = {
        "dia",
        "fecha_simulada",
        "tipo_hito",
        "titulo",
        "descripcion",
        "area_afectada",
        "severidad",
        "artefactos_relacionados",
        "decision_simulada",
        "requiere_revision_humana",
    }
    assert oblig.issubset(hitos[0].keys())
    assert all(h["severidad"] in SEVERIDADES for h in hitos)
    assert any(h["requiere_revision_humana"] for h in hitos)


def test_episodios_relacionan_crisis_privacidad_y_comparador():
    out = _tmp("episodios")
    narrativa, _ = ejecutar_desde_argumentos(_args_sin_entradas_existentes(out))
    episodios = narrativa["episodios_narrativos"]
    assert episodios
    assert any(ep["crisis_relacionadas"] for ep in episodios)
    assert any(ep["riesgos_privacidad_relacionados"] for ep in episodios)
    assert any(ep["comparativas_relacionadas"] for ep in episodios)


def test_mapa_evidencias_sinteticas_e_integra_proyectos():
    contexto_min = {
        "empresa": {"empresa": {"id_empresa": "EMP-X", "nombre": "Empresa X", "sector": "servicios"}},
        "eventos": [],
        "resumen_eventos": {},
        "documentos": [],
        "resumen_documentos": {},
        "escenarios": [],
        "resumen_escenarios": {},
        "crisis": [],
        "resumen_crisis": {},
        "revisiones": [],
        "registro_decisiones": [],
        "resumen_revision": {},
        "estado_operativo": {},
        "alertas": [],
        "decisiones": [],
        "resumen_gemelo": {},
        "inventario_privacidad": [],
        "riesgos_privacidad": [],
        "resumen_privacidad": {},
        "procesos_comparados": [],
        "comparaciones": [],
        "resumen_comparador": {},
    }
    narrativa = construir_demo_narrativa(
        contexto=contexto_min,
        seed=42,
        dias=7,
        base_repo=Path.cwd(),
        entradas_utilizadas={"entrada_empresa": "x"},
    )
    evidencias = narrativa["mapa_evidencias"]
    assert evidencias
    assert all(e["es_sintetica"] is True for e in evidencias)
    proyectos = {e["proyecto_origen"] for e in evidencias}
    assert len(proyectos) >= 3


def test_exportaciones_completas():
    out = _tmp("export")
    _, rutas = ejecutar_desde_argumentos(_args_sin_entradas_existentes(out))
    esperadas = [
        "demo_json",
        "linea_tiempo_json",
        "linea_tiempo_csv",
        "episodios_json",
        "episodios_csv",
        "mapa_evidencias_json",
        "mapa_evidencias_csv",
        "resumen_json",
        "guion_md",
        "expediente_md",
    ]
    for key in esperadas:
        assert Path(rutas[key]).exists()


def test_limites_explicitos_sin_api_claves_datos_reales_ni_productivo():
    out = _tmp("limites")
    narrativa, rutas = ejecutar_desde_argumentos(_args_sin_entradas_existentes(out))
    texto = json.dumps(narrativa, ensure_ascii=False).lower()
    assert "api_key" not in texto
    assert "token_secreto" not in texto
    assert "dato_personal_real" not in texto
    assert "agente_real_ejecutado" not in texto
    assert "cliente real confirmado" not in texto
    assert "recomendacion_empresarial_real" not in texto

    expediente = Path(rutas["expediente_md"]).read_text(encoding="utf-8").lower()
    assert "no existe sistema productivo" in expediente
    assert "no existe cliente real" in expediente

