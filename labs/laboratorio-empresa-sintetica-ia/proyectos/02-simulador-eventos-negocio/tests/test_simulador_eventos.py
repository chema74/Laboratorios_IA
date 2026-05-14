from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

RUTA_BASE = Path(__file__).resolve().parents[1]
RUTA_SRC = RUTA_BASE / "src"
if str(RUTA_SRC) not in sys.path:
    sys.path.insert(0, str(RUTA_SRC))

from simulador_eventos_negocio.cargador_empresa import cargar_empresa_sintetica
from simulador_eventos_negocio.exportador import exportar_eventos_json_csv, exportar_resumen_json
from simulador_eventos_negocio.simulador import construir_resumen_eventos, simular_eventos_negocio


def _tmp_local(nombre: str) -> Path:
    base = RUTA_BASE / "tests" / ".tmp"
    base.mkdir(parents=True, exist_ok=True)
    ruta = base / nombre
    if ruta.exists():
        shutil.rmtree(ruta)
    ruta.mkdir(parents=True, exist_ok=True)
    return ruta


def test_simulacion_devuelve_lista_eventos():
    empresa = cargar_empresa_sintetica("ruta/inexistente.json")
    eventos = simular_eventos_negocio(empresa, seed=42, dias=2, eventos_por_dia=3)
    assert isinstance(eventos, list)
    assert len(eventos) == 6


def test_reproducible_misma_seed():
    empresa = cargar_empresa_sintetica("ruta/inexistente.json")
    a = simular_eventos_negocio(empresa, seed=99, dias=2, eventos_por_dia=4)
    b = simular_eventos_negocio(empresa, seed=99, dias=2, eventos_por_dia=4)
    assert a == b


def test_campos_obligatorios_evento():
    empresa = cargar_empresa_sintetica("ruta/inexistente.json")
    evento = simular_eventos_negocio(empresa, seed=1, dias=1, eventos_por_dia=1)[0]
    obligatorios = {
        "id_evento", "tipo_evento", "fecha_evento", "severidad", "entidad_afectada",
        "id_entidad_afectada", "descripcion", "estado_evento", "origen_simulado",
        "requiere_revision_humana", "impacto_estimado",
    }
    assert obligatorios.issubset(evento.keys())


def test_varios_tipos_evento():
    empresa = cargar_empresa_sintetica("ruta/inexistente.json")
    eventos = simular_eventos_negocio(empresa, seed=7, dias=5, eventos_por_dia=6)
    tipos = {e["tipo_evento"] for e in eventos}
    assert len(tipos) >= 3


def test_resumen_contiene_campos_clave():
    empresa = cargar_empresa_sintetica("ruta/inexistente.json")
    eventos = simular_eventos_negocio(empresa, seed=13, dias=3, eventos_por_dia=5)
    resumen = construir_resumen_eventos(eventos)
    assert "total_eventos" in resumen
    assert "eventos_por_tipo" in resumen
    assert "eventos_por_severidad" in resumen


def test_exportaciones_crean_archivos():
    empresa = cargar_empresa_sintetica("ruta/inexistente.json")
    eventos = simular_eventos_negocio(empresa, seed=10, dias=2, eventos_por_dia=4)
    resumen = construir_resumen_eventos(eventos)
    carpeta = _tmp_local("salida")

    ruta_json, ruta_csv = exportar_eventos_json_csv(eventos, carpeta)
    ruta_resumen = exportar_resumen_json(resumen, carpeta)

    assert ruta_json.exists()
    assert ruta_json.name == "eventos_negocio.json"
    assert ruta_csv.exists()
    assert ruta_csv.name == "eventos_negocio.csv"
    assert ruta_resumen.exists()
    assert ruta_resumen.name == "resumen_eventos.json"


def test_sin_api_externa_ni_claves_ni_datos_reales():
    empresa = cargar_empresa_sintetica("ruta/inexistente.json")
    eventos = simular_eventos_negocio(empresa, seed=3, dias=2, eventos_por_dia=2)
    texto = json.dumps(eventos, ensure_ascii=False).lower()
    assert "api_key" not in texto
    assert "token" not in texto
    assert "password" not in texto
    assert "cliente ficticio" in json.dumps(empresa, ensure_ascii=False).lower()
