from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
LABS_ROOT = REPO_ROOT / "labs"


def run(cmd: list[str], cwd: Path, env: dict[str, str]) -> int:
    return subprocess.run(cmd, cwd=cwd, env=env).returncode


def _coverage_steps_for_lab(lab: Path) -> list[list[str]]:
    steps: list[list[str]] = []

    if (lab / "tests").exists():
        steps.append([sys.executable, "-m", "unittest", "discover", "tests", "-v"])

    project_tests = sorted(tests_dir for tests_dir in (lab / "proyectos").glob("**/tests") if any(tests_dir.glob("test_*.py")))
    if lab.name == "laboratorio-empresa-sintetica-ia" and project_tests:
        steps.append([sys.executable, str(REPO_ROOT / "scripts" / "run_function_tests.py"), "proyectos"])
    else:
        for tests_dir in project_tests:
            rel = tests_dir.relative_to(lab).as_posix()
            steps.append([sys.executable, "-m", "unittest", "discover", rel, "-v"])

    return steps


def main() -> None:
    tmp_dir = REPO_ROOT / ".tmp"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    reports_dir = REPO_ROOT / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    env = os.environ.copy()
    env["TMP"] = str(tmp_dir)
    env["TEMP"] = str(tmp_dir)
    env["PYTHONUTF8"] = "1"
    env["COVERAGE_FILE"] = str(REPO_ROOT / ".coverage")

    labs_with_tests = [lab for lab in sorted(p for p in LABS_ROOT.iterdir() if p.is_dir()) if _coverage_steps_for_lab(lab)]

    if not labs_with_tests:
        print("No se encontraron laboratorios con tests.")
        return

    rc = run([sys.executable, "-m", "coverage", "erase"], REPO_ROOT, env)
    if rc != 0:
        raise SystemExit(rc)

    for lab in labs_with_tests:
        print(f"=== COVERAGE: {lab.name} ===")
        lab_env = env.copy()
        lab_env["ARTIFACTS_DIR"] = str(REPO_ROOT / "artifacts" / lab.name)
        for step in _coverage_steps_for_lab(lab):
            rc = run([sys.executable, "-m", "coverage", "run", "--append", *step[1:]], lab, lab_env)
            if rc != 0:
                raise SystemExit(rc)

    rc = run([sys.executable, "-m", "coverage", "xml", "-o", "reports/coverage.xml"], REPO_ROOT, env)
    if rc != 0:
        raise SystemExit(rc)

    rc = run([sys.executable, "-m", "coverage", "report", "--fail-under=70"], REPO_ROOT, env)
    if rc != 0:
        raise SystemExit(rc)


if __name__ == "__main__":
    main()
