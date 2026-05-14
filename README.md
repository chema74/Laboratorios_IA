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
python -m pip install -U pip pre-commit
pre-commit install
pre-commit run --all-files
powershell -ExecutionPolicy Bypass -File scripts/run_operational_checks.ps1
```

## Alcance del runner operacional

`scripts/run_operational_checks.ps1`:

- detecta laboratorios bajo `labs/`;
- configura `TMP/TEMP` local en `.tmp`;
- ejecuta `python -m unittest discover tests -v` en cada laboratorio con carpeta `tests`;
- resume resultados y devuelve codigo de salida no-cero si hay fallos.

## Estandares en raiz

- `pyproject.toml`: configuracion de `ruff`.
- `.pre-commit-config.yaml`: hooks basicos de higiene y lint.
- `.github/workflows/ci.yml`: pipeline de comprobaciones en cada push/PR.
