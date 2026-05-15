from __future__ import annotations

import argparse
import importlib.util
import traceback
from collections.abc import Callable
from pathlib import Path


def _load_module(path: Path):
    module_name = "function_tests_" + "_".join(path.with_suffix("").parts[-6:])
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"No se pudo cargar {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _test_functions(module) -> list[tuple[str, Callable[[], None]]]:
    tests: list[tuple[str, Callable[[], None]]] = []
    for name in sorted(dir(module)):
        value = getattr(module, name)
        if name.startswith("test_") and callable(value):
            tests.append((name, value))
    return tests


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", help="Directorios o archivos test_*.py a ejecutar.")
    args = parser.parse_args()

    files: list[Path] = []
    for raw in args.paths:
        path = Path(raw)
        if path.is_file():
            files.append(path)
        else:
            files.extend(sorted(path.glob("**/test_*.py")))

    total = 0
    failures: list[str] = []
    for file_path in files:
        try:
            module = _load_module(file_path)
            tests = _test_functions(module)
            for name, func in tests:
                total += 1
                try:
                    func()
                    print(f"ok {file_path}:{name}")
                except Exception:
                    failures.append(f"{file_path}:{name}\n{traceback.format_exc()}")
                    print(f"FAIL {file_path}:{name}")
        except Exception:
            failures.append(f"{file_path}:<import>\n{traceback.format_exc()}")
            print(f"FAIL {file_path}:<import>")

    print(f"Function tests ejecutados: {total}. Fallos: {len(failures)}.")
    if failures:
        print("\n\n".join(failures))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
