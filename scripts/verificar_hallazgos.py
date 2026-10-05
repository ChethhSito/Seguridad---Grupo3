"""Comprueba que el laboratorio siga produciendo sus dos hallazgos didacticos."""

import json
import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "laboratorio-sql-fstring",
    "laboratorio-html-markup-fstring",
}


def semgrep_binary():
    folder = "Scripts" if os.name == "nt" else "bin"
    name = "semgrep.exe" if os.name == "nt" else "semgrep"
    candidate = ROOT / ".venv" / folder / name
    return str(candidate) if candidate.exists() else "semgrep"


def normalize(check_id):
    name = check_id.replace("\\", "/").split("/")[-1]
    prefix = "reglas."
    return name[len(prefix):] if name.startswith(prefix) else name


def main():
    environment = os.environ.copy()
    environment["PYTHONIOENCODING"] = "utf-8"
    command = [
        semgrep_binary(), "scan", "--config", "reglas.yml", "--json",
        "--metrics=off", "app.py",
    ]
    scan = subprocess.run(
        command, cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
        errors="replace", env=environment, check=False,
    )
    if not scan.stdout:
        print(scan.stderr, file=sys.stderr)
        print(
            "Semgrep no produjo un reporte. En Windows, Smart App Control puede estar bloqueando semgrep-core.exe.",
            file=sys.stderr,
        )
        return scan.returncode or 1

    report = json.loads(scan.stdout)
    if report.get("errors"):
        print(report["errors"], file=sys.stderr)
        return 1
    observed = [normalize(item["check_id"]) for item in report["results"]]
    if len(observed) != 2 or set(observed) != EXPECTED:
        print(f"Hallazgos inesperados: {observed}", file=sys.stderr)
        return 1

    print("OK: se detectaron los dos patrones inseguros esperados.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
