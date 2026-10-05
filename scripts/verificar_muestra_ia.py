"""Comprueba la muestra generada por IA y exige sus hallazgos didacticos."""

import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    "muestras/codigo_generado_ia.py",
    "muestras/dependencias-ia.txt",
]
EXPECTED = {
    "laboratorio-sql-fstring",
    "laboratorio-html-markup-fstring",
    "laboratorio-hash-md5",
    "laboratorio-password-fijo",
    "laboratorio-debug-flask",
    "laboratorio-pickle",
    "laboratorio-log-credencial",
    "laboratorio-acceso-por-parametro",
    "laboratorio-assert-autorizacion",
    "laboratorio-urlopen-destino",
    "laboratorio-dependencia-antigua",
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


def scan():
    environment = os.environ.copy()
    environment["PYTHONIOENCODING"] = "utf-8"
    command = [
        semgrep_binary(), "scan", "--config", "reglas.yml", "--json",
        "--metrics=off", *TARGETS,
    ]
    result = subprocess.run(
        command, cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
        errors="replace", env=environment, check=False,
    )
    if not result.stdout:
        print(result.stderr, file=sys.stderr)
        return None, result.returncode or 1
    report = json.loads(result.stdout)
    if report.get("errors"):
        print(report["errors"], file=sys.stderr)
        return None, 1
    return report["results"], 0


def main():
    findings, status = scan()
    if findings is None:
        return status
    observed = {normalize(item["check_id"]) for item in findings}
    if observed != EXPECTED:
        missing = sorted(EXPECTED - observed)
        extra = sorted(observed - EXPECTED)
        print(f"Faltan: {missing}", file=sys.stderr)
        print(f"Sobran: {extra}", file=sys.stderr)
        return 1
    print(f"OK: la muestra de IA produjo los {len(EXPECTED)} hallazgos esperados.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
