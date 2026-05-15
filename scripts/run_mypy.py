from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
LABS_ROOT = REPO_ROOT / "labs"


def main() -> None:
    targets: list[str] = []

    for py in sorted((REPO_ROOT / "scripts").glob("*.py")):
        targets.append(str(py.relative_to(REPO_ROOT)))

    for run_all in sorted(LABS_ROOT.glob("**/scripts/run_all.py")):
        targets.append(str(run_all.relative_to(REPO_ROOT)))

    if not targets:
        print("No hay objetivos para mypy.")
        return

    for target in targets:
        cmd = [sys.executable, "-m", "mypy", "--config-file", "mypy.ini", target]
        rc = subprocess.run(cmd, cwd=REPO_ROOT).returncode
        if rc != 0:
            raise SystemExit(rc)


if __name__ == "__main__":
    main()
