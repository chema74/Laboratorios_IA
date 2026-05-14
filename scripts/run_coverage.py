from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LABS_ROOT = REPO_ROOT / "labs"


def run(cmd: list[str], cwd: Path, env: dict[str, str]) -> int:
    return subprocess.run(cmd, cwd=cwd, env=env).returncode


def main() -> None:
    tmp_dir = REPO_ROOT / ".tmp"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    reports_dir = REPO_ROOT / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    env = os.environ.copy()
    env["TMP"] = str(tmp_dir)
    env["TEMP"] = str(tmp_dir)
    env["PYTHONUTF8"] = "1"

    labs_with_tests: list[Path] = []
    for lab in sorted(p for p in LABS_ROOT.iterdir() if p.is_dir()):
        if (lab / "tests").exists():
            labs_with_tests.append(lab)

    if not labs_with_tests:
        print("No se encontraron laboratorios con tests.")
        return

    rc = run([sys.executable, "-m", "coverage", "erase"], REPO_ROOT, env)
    if rc != 0:
        raise SystemExit(rc)

    for lab in labs_with_tests:
        print(f"=== COVERAGE: {lab.name} ===")
        rc = run(
            [
                sys.executable,
                "-m",
                "coverage",
                "run",
                "--append",
                "-m",
                "unittest",
                "discover",
                "tests",
                "-v",
            ],
            lab,
            env,
        )
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
