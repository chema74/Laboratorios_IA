from __future__ import annotations

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPO_ROOT / "schemas" / "manifest.json"


def _read_json(path: Path) -> object:
    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


class TestJsonContracts(unittest.TestCase):
    def test_manifest_shape_and_uniqueness(self) -> None:
        manifest = _read_json(MANIFEST_PATH)
        self.assertIsInstance(manifest, list, "El manifiesto debe ser una lista.")
        self.assertGreater(len(manifest), 0, "El manifiesto no puede estar vacio.")

        names: set[str] = set()
        for idx, item in enumerate(manifest):
            self.assertIsInstance(item, dict, f"Entrada {idx} del manifiesto debe ser objeto.")
            for key in ("name", "data_file", "schema_file"):
                self.assertIn(key, item, f"Falta '{key}' en entrada {idx}.")
                self.assertIsInstance(item[key], str, f"'{key}' en entrada {idx} debe ser string.")
                self.assertTrue(item[key].strip(), f"'{key}' en entrada {idx} no puede ser vacio.")

            name = item["name"]
            self.assertNotIn(name, names, f"Nombre de contrato duplicado: {name}")
            names.add(name)

    def test_all_manifest_entries_validate(self) -> None:
        manifest = _read_json(MANIFEST_PATH)
        failures: list[str] = []

        for item in manifest:
            name = str(item["name"])
            data_file = REPO_ROOT / str(item["data_file"])
            schema_file = REPO_ROOT / str(item["schema_file"])

            if not data_file.exists():
                failures.append(f"{name}: data_file inexistente -> {data_file}")
                continue
            if not schema_file.exists():
                failures.append(f"{name}: schema_file inexistente -> {schema_file}")
                continue

            data = _read_json(data_file)
            schema = _read_json(schema_file)
            validator = Draft202012Validator(schema)
            errors = sorted(validator.iter_errors(data), key=lambda e: e.path)
            if errors:
                first = errors[0]
                path = "/".join(str(p) for p in first.path) or "<root>"
                failures.append(f"{name}: {first.message} (path={path})")

        self.assertEqual(
            failures,
            [],
            "Contratos JSON invalidos:\n- " + "\n- ".join(failures),
        )


if __name__ == "__main__":
    unittest.main()
