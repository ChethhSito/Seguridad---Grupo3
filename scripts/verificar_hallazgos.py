"""Comprueba que el laboratorio siga produciendo sus dos hallazgos didacticos."""

import json
import os
import subprocess
import sys


EXPECTED = {
    "laboratorio-sql-fstring",
    "laboratorio-html-markup-fstring",
}


def main():
    command = ["semgrep", "scan", "--config", "reglas.yml", "--json", "app.py"]
    environment = os.environ.copy()
    environment["PYTHONIOENCODING"] = "utf-8"
    scan = subprocess.run(
        command, capture_output=True, text=True, encoding="utf-8", errors="replace",
        env=environment, check=False
    )
    if scan.returncode != 0:
        print(scan.stderr, file=sys.stderr)
        return scan.returncode

    report = json.loads(scan.stdout)
    findings = report["results"]
    observed = [item["check_id"] for item in findings]
    if len(observed) != 2 or set(observed) != EXPECTED:
        print(f"Hallazgos inesperados: {observed}", file=sys.stderr)
        return 1

    print("OK: se detectaron los dos patrones inseguros esperados.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
