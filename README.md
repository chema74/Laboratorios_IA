# Laboratorios IA - Operacion Unificada

Monorepo con laboratorios locales de IA orientados a pruebas, trazabilidad y demostraciones reproducibles.

## Objetivo operativo

Este repositorio queda preparado para:

- ejecutar validaciones de forma consistente en Windows;
- estandarizar calidad minima de Python;
- soportar CI automatizada en GitHub Actions;
- reducir fallos por entorno temporal (`TMP/TEMP`) y codificacion.

## Ejecucion rapida

```powershell
python -m pip install -U pip
pip install -r requirements-dev.txt
pre-commit install
pre-commit run --all-files
powershell -ExecutionPolicy Bypass -File scripts/run_operational_checks.ps1
```

## Alcance del runner operacional

`scripts/run_operational_checks.ps1`:

- detecta laboratorios bajo `labs/`;
- configura `TMP/TEMP` local en `.tmp`;
- ejecuta `python scripts/run_all.py` por laboratorio;
- resume resultados y devuelve codigo de salida no-cero si hay fallos.
- exporta `reports/operational_summary.json`.

Variables utiles:

- `RUN_DEMOS=1`: activa demos dentro de `run_all.py`.

## Matriz de operacion por laboratorio

| Laboratorio | Demo principal | Tests | Salud |
|---|---|---|---|
| `laboratorio-agentes-enterprise-local` | `python scripts\ejecutar_demo.py` | `python -m unittest discover tests -v` | `python scripts\comprobar_salud.py` |
| `laboratorio-backend-ia-empresarial` | `python scripts\ejecutar_demo.py` | `python -m unittest discover tests -v` | `python scripts\comprobar_salud.py` |
| `laboratorio-empresa-sintetica-ia` | `python proyectos\10-demo-narrativa-empresa-completa\ejecutar_demo.py` | tests por proyecto en `proyectos\**\tests` | `python scripts\comprobar_salud.py` |
| `laboratorio-evaluacion-llm-local` | `python scripts\ejecutar_demo.py` | `python -m unittest discover tests -v` | `python scripts\comprobar_salud.py` |
| `laboratorio-gobernanza-ai-act-local` | `python scripts\ejecutar_demo.py` | `python -m unittest discover tests -v` | `python scripts\comprobar_salud.py` |
| `laboratorio-google-ia-empresarial` | demos por proyecto en `proyectos\**\README.md` | n/a (V1 documental) | `python scripts\comprobar_salud.py` |
| `laboratorio-microsoft-ia-empresarial` | demos por proyecto en `proyectos\**\README.md` | n/a (V1 documental) | `python scripts\comprobar_salud.py` |
| `laboratorio-observabilidad-costes-ia` | `python scripts\ejecutar_demo.py` | `python -m unittest discover tests -v` | `python scripts\comprobar_salud.py` |
| `laboratorio-privacidad-datos-ia` | `python scripts\ejecutar_demo.py` | `python -m unittest discover tests -v` | `python scripts\comprobar_salud.py` |
| `laboratorio-rag-corporativo-local` | `python scripts\ejecutar_demo.py` | `python -m unittest discover tests -v` | `python scripts\comprobar_salud.py` |
| `laboratorio-seguridad-agentes-ia` | demos por proyecto en `proyectos\**\README.md` | tests por proyecto en `proyectos\**\tests` | `python scripts\comprobar_salud.py` |

## Estandares en raiz

- `pyproject.toml`: configuracion de `ruff`.
- `.pre-commit-config.yaml`: hooks basicos de higiene y lint.
- `.github/workflows/ci.yml`: pipeline de comprobaciones en cada push/PR.
- `constraints.txt`: versionado base para tooling.
- `CHANGELOG.md`: registro de cambios operativos.

## Calidad avanzada

- Cobertura transversal: `python scripts/run_coverage.py` (umbral minimo 70%).
- CI en matriz: Windows y Ubuntu con Python 3.11 y 3.12.
- Gate de limpieza: el workflow falla si quedan cambios tracked tras los checks.
