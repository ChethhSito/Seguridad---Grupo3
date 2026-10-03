"""Genera un HTML autocontenido a partir de dos escaneos reales de Semgrep."""

import html
import json
import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "reportes" / "semgrep.html"
SOURCE = ROOT / "app.py"

COMMUNITY_EXPLANATIONS = {
    "python.django.security.injection.sql.sql-injection-using-db-cursor-execute.sql-injection-db-cursor-execute":
        "Una entrada de la petición llega a execute() dentro de una consulta SQL. La consulta podría cambiar por los datos ingresados. En este laboratorio se corrige con parámetros de sqlite3; la referencia a Django en la regla original no aplica a esta aplicación Flask.",
    "python.lang.security.audit.formatted-sql-query.formatted-sql-query":
        "La consulta SQL se construye con formato de texto. Usa parámetros para separar el dato de la instrucción SQL.",
    "python.sqlalchemy.security.sqlalchemy-execute-raw-query.sqlalchemy-execute-raw-query":
        "La regla advierte sobre SQL construido con datos no confiables. Aunque menciona SQLAlchemy, este laboratorio usa sqlite3; la corrección correspondiente es una consulta parametrizada.",
    "python.django.security.injection.tainted-sql-string.tainted-sql-string":
        "La entrada del usuario se incorpora manualmente a una cadena SQL. Esto puede alterar la consulta. La recomendación aplicable aquí es usar parámetros de sqlite3, aunque la regla se originó para Django.",
    "python.flask.security.injection.tainted-sql-string.tainted-sql-string":
        "La entrada del usuario se incorpora manualmente a una consulta SQL en Flask. Usa una consulta parametrizada para evitar que el valor cambie la instrucción.",
    "python.flask.security.xss.audit.explicit-unescape-with-markup.explicit-unescape-with-markup":
        "Markup() trata el HTML interpolado como seguro y evita el escape. Si la entrada procede del usuario, puede mostrarse como HTML ejecutable. Usa una plantilla con autoescape.",
    "python.django.security.injection.raw-html-format.raw-html-format":
        "La entrada del usuario aparece dentro de HTML construido manualmente. Esto puede permitir XSS. La regla menciona Django, pero en esta aplicación Flask se usa una plantilla con autoescape.",
    "python.flask.security.injection.raw-html-concat.raw-html-format":
        "La entrada del usuario aparece dentro de HTML construido manualmente en Flask. Utiliza render_template con una variable normal para que Jinja escape el contenido.",
}


def esc(value):
    return html.escape(str(value), quote=True)


def semgrep_binary():
    candidate = Path(sys.executable).with_name("semgrep.exe" if os.name == "nt" else "semgrep")
    return str(candidate) if candidate.exists() else "semgrep"


def scan(config):
    environment = os.environ.copy()
    environment["PYTHONIOENCODING"] = "utf-8"
    command = [semgrep_binary(), "scan", "--config", config, "--json", "app.py"]
    result = subprocess.run(
        command, cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
        errors="replace", env=environment, check=False
    )
    if result.returncode:
        raise RuntimeError(f"Fallo el escaneo ({config}):\n{result.stderr}")
    report = json.loads(result.stdout)
    if report.get("errors"):
        raise RuntimeError(f"Semgrep devolvio errores ({config}): {report['errors']}")
    return report["results"]


def kind(item):
    rule = item["check_id"].lower()
    if "sql" in rule:
        return "SQL injection", "sql"
    if "html" in rule or "xss" in rule or "markup" in rule:
        return "XSS / HTML", "xss"
    return "Otro aviso", "other"


def context(source_lines, start, end):
    first = max(1, start - 2)
    last = min(len(source_lines), end + 2)
    rows = []
    for number in range(first, last + 1):
        active = " active" if start <= number <= end else ""
        rows.append(
            f'<span class="code-line{active}"><span class="line-no">{number:03}</span>'
            f'<span>{esc(source_lines[number - 1])}</span></span>'
        )
    return "\n".join(rows)


def card(item, source_lines, index, community=False):
    label, category = kind(item)
    start = item["start"]["line"]
    end = item["end"]["line"]
    original_message = item.get("extra", {}).get("message", "Sin descripción")
    message = COMMUNITY_EXPLANATIONS.get(item["check_id"], original_message) if community else original_message
    original = (
        f'<details><summary>Ver mensaje original de Semgrep (inglés)</summary>'
        f'<p>{esc(original_message)}</p></details>'
        if community and item["check_id"] in COMMUNITY_EXPLANATIONS else ""
    )
    severity = item.get("extra", {}).get("severity", "INFO")
    return f"""
    <article class="finding" data-category="{category}">
      <div class="finding-head">
        <div class="finding-num">{index:02}</div>
        <div class="finding-title"><span class="pill {category}">{esc(label)}</span>
          <h3>{esc(item['check_id'])}</h3></div>
        <span class="severity">{esc(severity)}</span>
      </div>
      <p class="message">{esc(message)}</p>
      {original}
      <div class="location">app.py · línea {start}{f'–{end}' if end != start else ''}</div>
      <pre><code>{context(source_lines, start, end)}</code></pre>
    </article>"""


def main():
    custom = scan("reglas.yml")
    community = scan("auto")
    source_lines = SOURCE.read_text(encoding="utf-8").splitlines()
    custom_cards = "".join(card(item, source_lines, i) for i, item in enumerate(custom, 1))
    community_cards = "".join(card(item, source_lines, i, community=True) for i, item in enumerate(community, 1))
    page = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Reporte Semgrep · Grupo 3</title>
  <style>
    :root {{ color-scheme: light; --ink:#182a37; --muted:#657783; --line:#dbe3e8; --navy:#0c2533; --teal:#047f72; --paper:#f4f7f8; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; background:var(--paper); color:var(--ink); font:16px/1.55 system-ui,-apple-system,Segoe UI,sans-serif; }}
    header {{ background:linear-gradient(125deg,#0c2533,#154755); color:#fff; padding:42px max(24px,calc((100vw - 1100px)/2)); }}
    .eyebrow {{ color:#8de2ce; text-transform:uppercase; letter-spacing:.16em; font-size:.78rem; font-weight:800; }}
    h1 {{ margin:.35rem 0 .3rem; font-size:clamp(2rem,5vw,3.2rem); letter-spacing:-.04em; }}
    .subtitle {{ max-width:700px; color:#c5d9df; margin:0; }}
    main {{ max-width:1100px; margin:0 auto; padding:30px 24px 70px; }}
    .stats {{ display:grid; grid-template-columns:repeat(3,1fr); gap:14px; margin:-55px 0 32px; position:relative; }}
    .stat {{ background:#fff; border:1px solid var(--line); border-radius:16px; padding:18px 22px; box-shadow:0 9px 24px #0d2b3a11; }}
    .stat strong {{ display:block; font-size:2rem; line-height:1.15; color:#123f4a; }}
    .stat span {{ color:var(--muted); font-size:.9rem; }}
    .notice {{ border-left:4px solid var(--teal); background:#e8f5f1; padding:14px 18px; border-radius:0 10px 10px 0; margin-bottom:32px; }}
    h2 {{ font-size:1.55rem; letter-spacing:-.02em; margin:36px 0 4px; }}
    .section-intro {{ color:var(--muted); margin:0 0 18px; }}
    .finding {{ background:#fff; border:1px solid var(--line); border-radius:16px; padding:22px; margin:14px 0; box-shadow:0 4px 14px #0d2b3a08; }}
    .finding-head {{ display:flex; align-items:start; gap:14px; }}
    .finding-num {{ background:#eef3f5; border-radius:10px; padding:6px 10px; color:#43606c; font-weight:800; }}
    .finding-title {{ min-width:0; flex:1; }}
    h3 {{ font-size:1rem; overflow-wrap:anywhere; margin:7px 0 0; }}
    .pill,.severity {{ font-size:.75rem; font-weight:800; letter-spacing:.02em; border-radius:999px; padding:3px 9px; }}
    .pill.sql {{ background:#fff0dc; color:#92500a; }} .pill.xss {{ background:#fce9ef; color:#a22c53; }} .pill.other {{ background:#e9ecff; color:#374ca0; }}
    .severity {{ color:#9a3043; background:#fff0f1; }}
    .message {{ margin:14px 0 9px; }} .location {{ color:var(--muted); font-size:.9rem; margin-bottom:9px; }}
    details {{ color:var(--muted); font-size:.88rem; margin:8px 0 13px; }} summary {{ cursor:pointer; }} details p {{ margin:8px 0; }}
    pre {{ margin:0; background:#102b3b; color:#e9f3f6; border-radius:10px; padding:12px 0; overflow-x:auto; font:13px/1.55 Consolas,monospace; }}
    .code-line {{ display:flex; padding:0 14px; white-space:pre; }} .code-line.active {{ background:#185069; border-left:3px solid #59d3b6; padding-left:11px; }}
    .line-no {{ flex:none; width:45px; color:#91aebc; user-select:none; }}
    .explain {{ display:grid; grid-template-columns:repeat(2,1fr); gap:16px; }}
    .explain div {{ background:#fff; border:1px solid var(--line); border-radius:14px; padding:18px; }}
    .explain strong {{ display:block; margin-bottom:5px; }}
    footer {{ color:var(--muted); font-size:.9rem; margin-top:40px; border-top:1px solid var(--line); padding-top:18px; }}
    @media(max-width:650px) {{ .stats,.explain {{ grid-template-columns:1fr; }} .stats {{ margin:18px 0; }} header {{ padding:30px 24px; }} .finding-head {{ flex-wrap:wrap; }} }}
  </style>
</head>
<body>
<header><div class="eyebrow">Seguridad informática · Parcial · Grupo 3</div><h1>Hallazgos de Semgrep</h1>
<p class="subtitle">Resultado del análisis estático de <strong>app.py</strong>. Ejemplos vulnerables creados para un laboratorio local.</p></header>
<main>
  <div class="stats"><div class="stat"><strong>{len(custom)}</strong><span>Hallazgos con reglas propias</span></div>
  <div class="stat"><strong>{len(community)}</strong><span>Avisos con reglas comunitarias</span></div>
  <div class="stat"><strong>2</strong><span>Zonas inseguras preparadas</span></div></div>
  <div class="notice"><strong>Cómo leer el reporte.</strong> Los avisos comunitarios pueden señalar varias veces el mismo fragmento. {len(community)} avisos no significan {len(community)} vulnerabilidades distintas. Revisa cada resultado en su contexto.</div>
  <h2>Reglas del proyecto</h2><p class="section-intro">Dos patrones diseñados para explicar la diferencia entre código inseguro y corregido.</p>
  {custom_cards}
  <h2>Reglas comunitarias</h2><p class="section-intro">Explicaciones en español de los avisos de <code>--config auto</code>. Conservamos los identificadores y el mensaje original para poder comprobar cada resultado. El número puede cambiar cuando Semgrep actualice sus reglas.</p>
  {community_cards}
  <h2>Cómo se corrigieron los ejemplos</h2>
  <div class="explain"><div><strong>Consulta SQL</strong>La ruta segura usa <code>WHERE username = ?</code> y entrega el nombre como parámetro separado. Así el dato no se interpreta como parte de la instrucción SQL.</div>
  <div><strong>Salida HTML</strong>La ruta segura usa <code>render_template</code> con una variable en <code>templates/saludo.html</code>; Jinja escapa caracteres HTML de la entrada.</div></div>
  <footer>Reporte generado localmente por <code>scripts/generar_reporte.py</code>. Fuente: Semgrep CLI y <code>app.py</code>. Para actualizarlo, vuelve a ejecutar el generador.</footer>
</main></body></html>"""
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(page, encoding="utf-8")
    print(f"Reporte creado: {OUTPUT} ({len(custom)} reglas propias, {len(community)} avisos comunitarios)")


if __name__ == "__main__":
    main()
