"""Falla si el codigo corregido vuelve a coincidir con las reglas del laboratorio."""

import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    "muestras/referencias_seguras.py",
    "muestras/dependencias-seguras.txt",
]


def semgrep_binary():
    folder = "Scripts" if os.name == "nt" else "bin"
    name = "semgrep.exe" if os.name == "nt" else "semgrep"
    candidate = ROOT / ".venv" / folder / name
    return str(candidate) if candidate.exists() else "semgrep"


def main():
    environment = os.environ.copy()
    environment["PYTHONIOENCODING"] = "utf-8"
    command = [
        semgrep_binary(), "scan", "--config", "reglas.yml", "--error",
        "--metrics=off", *TARGETS,
    ]
    result = subprocess.run(
        command, cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
        errors="replace", env=environment, check=False,
    )
    if result.returncode == 0:
        print("OK: el codigo corregido no dispara las reglas del laboratorio.")
        return 0
    output = f"{result.stdout or ''}{result.stderr or ''}".strip()
    if result.returncode == 1:
        print("BLOQUEO: el codigo corregido volvio a coincidir con una regla.", file=sys.stderr)
        if output:
            print(output, file=sys.stderr)
        return 1
    print(
        "Semgrep no pudo ejecutarse. En Windows, Smart App Control puede estar bloqueando semgrep-core.exe.",
        file=sys.stderr,
    )
    if output:
        print(output, file=sys.stderr)
    return result.returncode or 1


if __name__ == "__main__":
    raise SystemExit(main())
