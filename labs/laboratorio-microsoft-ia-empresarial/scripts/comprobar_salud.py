from pathlib import Path

BASE = Path(__file__).resolve().parents[1]


def main() -> None:
    checks = [
        ("README", (BASE / "README.md").exists()),
        ("CATALOGO", (BASE / "CATALOGO.md").exists()),
        ("docs", (BASE / "docs").is_dir()),
        ("plantillas", (BASE / "plantillas").is_dir()),
        ("proyectos", (BASE / "proyectos").is_dir()),
        ("requirements", (BASE / "requirements.txt").exists()),
        ("readmes proyectos", len(list((BASE / "proyectos").glob("**/README.md"))) > 0),
    ]

    fallos = [nombre for nombre, ok in checks if not ok]
    for nombre, ok in checks:
        print(f"[{'OK' if ok else 'FAIL'}] {nombre}")

    if fallos:
        raise SystemExit(f"Salud fallida: {', '.join(fallos)}")

    print("Chequeo de salud correcto.")


if __name__ == "__main__":
    main()
