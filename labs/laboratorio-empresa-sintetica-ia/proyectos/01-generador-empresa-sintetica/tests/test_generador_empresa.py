from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

RUTA_BASE = Path(__file__).resolve().parents[1]
RUTA_SRC = RUTA_BASE / "src"
if str(RUTA_SRC) not in sys.path:
    sys.path.insert(0, str(RUTA_SRC))

from generador_empresa_sintetica.exportador import exportar_empresa_json, exportar_tablas_csv
from generador_empresa_sintetica.generador import generar_empresa_sintetica


def _crear_directorio_temporal_local(nombre: str) -> Path:
    """Crea carpeta temporal dentro del proyecto para evitar permisos externos."""
    raiz_tmp = RUTA_BASE / "tests" / ".tmp"
    raiz_tmp.mkdir(parents=True, exist_ok=True)
    destino = raiz_tmp / nombre
    if destino.exists():
        shutil.rmtree(destino)
    destino.mkdir(parents=True, exist_ok=True)
    return destino


def test_estructura_principal():
    resultado = generar_empresa_sintetica(seed=42, numero_empleados=5, numero_clientes=7, numero_productos=3)
    claves = {"empresa", "empleados", "clientes", "productos", "procesos", "resumen_operativo"}
    assert claves.issubset(resultado.keys())


def test_reproducibilidad_misma_seed():
    a = generar_empresa_sintetica(seed=99, numero_empleados=6, numero_clientes=8, numero_productos=4)
    b = generar_empresa_sintetica(seed=99, numero_empleados=6, numero_clientes=8, numero_productos=4)
    assert a == b


def test_cantidades_solicitadas():
    resultado = generar_empresa_sintetica(seed=11, numero_empleados=12, numero_clientes=20, numero_productos=8)
    assert len(resultado["empleados"]) == 12
    assert len(resultado["clientes"]) == 20
    assert len(resultado["productos"]) == 8


def test_exportacion_json_crea_archivo():
    carpeta = _crear_directorio_temporal_local("json")
    resultado = generar_empresa_sintetica(seed=50)
    ruta = exportar_empresa_json(resultado, carpeta)
    assert ruta.exists()
    contenido = json.loads(ruta.read_text(encoding="utf-8"))
    assert "empresa" in contenido


def test_exportacion_csv_crea_archivos():
    carpeta = _crear_directorio_temporal_local("csv")
    resultado = generar_empresa_sintetica(seed=70)
    rutas = exportar_tablas_csv(resultado, carpeta)
    esperados = {"empleados.csv", "clientes.csv", "productos.csv", "procesos.csv"}
    nombres = {r.name for r in rutas}
    assert esperados == nombres
    for ruta in rutas:
        assert ruta.exists()


def test_no_datos_reales_ni_claves_ni_api_externa():
    resultado = generar_empresa_sintetica(seed=1, numero_empleados=3, numero_clientes=3, numero_productos=2)
    texto = json.dumps(resultado, ensure_ascii=False).lower()
    assert "ficticio" in texto or "sintetica" in texto
    assert "api_key" not in texto
    assert "token" not in texto
    assert "password" not in texto
