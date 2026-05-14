from pathlib import Path

BASE = Path(__file__).resolve().parents[1]


def main() -> None:
    checks = [
        ("README", (BASE / "README.md").exists()),
        ("CATALOGO", (BASE / "CATALOGO.md").exists()),
        ("datos_ejemplo", (BASE / "datos_ejemplo").is_dir()),
        ("proyectos", (BASE / "proyectos").is_dir()),
        ("docs", (BASE / "docs").is_dir()),
        ("tests proyectos", len(list((BASE / "proyectos").glob("**/tests/test_*.py"))) > 0),
        ("demos proyectos", len(list((BASE / "proyectos").glob("**/ejecutar_demo.py"))) > 0),
    ]

    fallos = [nombre for nombre, ok in checks if not ok]
    for nombre, ok in checks:
        print(f"[{'OK' if ok else 'FAIL'}] {nombre}")

    if fallos:
        raise SystemExit(f"Salud fallida: {', '.join(fallos)}")

    print("Chequeo de salud correcto.")


if __name__ == "__main__":
    main()
