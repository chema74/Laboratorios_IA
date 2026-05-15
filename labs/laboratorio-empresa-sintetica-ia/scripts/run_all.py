import argparse
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]


def _run(cmd: list[str]) -> int:
    return subprocess.run(cmd, cwd=BASE).returncode


def _project_test_steps() -> list[tuple[str, list[str]]]:
    steps: list[tuple[str, list[str]]] = []
    for tests_dir in sorted((BASE / "proyectos").glob("**/tests")):
        if any(tests_dir.glob("test_*.py")):
            rel = tests_dir.relative_to(BASE).as_posix()
            steps.append((f"tests:{rel}", [sys.executable, "-m", "pytest", rel, "-q"]))
    return steps


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--with-demo", action="store_true")
    args = parser.parse_args()

    steps = [("salud", [sys.executable, "scripts/comprobar_salud.py"])]
    tests_dir = BASE / "tests"
    if tests_dir.exists():
        steps.append(("tests", [sys.executable, "-m", "unittest", "discover", "tests", "-v"]))
    steps.extend(_project_test_steps())
    demo_proyecto = BASE / "proyectos" / "10-demo-narrativa-empresa-completa" / "ejecutar_demo.py"
    if args.with_demo and demo_proyecto.exists():
        steps.append(
            (
                "demo",
                [sys.executable, "proyectos/10-demo-narrativa-empresa-completa/ejecutar_demo.py"],
            )
        )

    for name, cmd in steps:
        print(f"== {name.upper()} ==")
        if _run(cmd) != 0:
            raise SystemExit(1)


if __name__ == "__main__":
    main()
