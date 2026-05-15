from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPO_ROOT / "schemas" / "manifest.json"


def _read_json(path: Path) -> object:
    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def main() -> None:
    manifest = _read_json(MANIFEST_PATH)
    if not isinstance(manifest, list):
        raise SystemExit("Manifest de esquemas invalido: se esperaba una lista.")

    failed = False
    for item in manifest:
        if not isinstance(item, dict):
            print("[FAIL] Entrada de manifest invalida (no objeto).")
            failed = True
            continue

        name = str(item.get("name", "sin_nombre"))
        data_file = REPO_ROOT / str(item.get("data_file", ""))
        schema_file = REPO_ROOT / str(item.get("schema_file", ""))

        if not data_file.exists():
            print(f"[FAIL] {name}: no existe data file {data_file}")
            failed = True
            continue
        if not schema_file.exists():
            print(f"[FAIL] {name}: no existe schema file {schema_file}")
            failed = True
            continue

        data = _read_json(data_file)
        schema = _read_json(schema_file)
        validator = Draft202012Validator(schema)
        errors = sorted(validator.iter_errors(data), key=lambda e: e.path)
        if errors:
            failed = True
            first = errors[0]
            path = "/".join(str(p) for p in first.path) or "<root>"
            print(f"[FAIL] {name}: {first.message} (path={path})")
        else:
            print(f"[OK] {name}")

    if failed:
        raise SystemExit(1)

    print("Validacion de contratos JSON correcta.")


if __name__ == "__main__":
    main()
