# Changelog

## 2026-05-14

- Se unifica la operacion del monorepo con `scripts/run_operational_checks.ps1`.
- Se añade contrato `scripts/run_all.py` por laboratorio.
- Se incorporan `comprobar_salud.py` para laboratorios documentales faltantes.
- Se publica resumen operacional JSON en `reports/operational_summary.json`.
- Se endurece lectura de JSON en RAG para BOM UTF-8 (`utf-8-sig`).
- Se añade base de calidad: `pyproject.toml`, pre-commit y CI en GitHub Actions.
