import argparse
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]


def _run(cmd: list[str]) -> int:
    return subprocess.run(cmd, cwd=BASE).returncode


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--with-demo", action="store_true")
    args = parser.parse_args()

    steps = [
        ("salud", [sys.executable, "scripts/comprobar_salud.py"]),
        ("tests", [sys.executable, "-m", "unittest", "discover", "tests", "-v"]),
    ]
    if args.with_demo:
        steps.append(("demo", [sys.executable, "scripts/ejecutar_demo.py"]))

    for name, cmd in steps:
        print(f"== {name.upper()} ==")
        if _run(cmd) != 0:
            raise SystemExit(1)


if __name__ == "__main__":
    main()
