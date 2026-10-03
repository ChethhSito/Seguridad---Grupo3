"""Laboratorio local: dos rutas vulnerables y sus versiones corregidas."""

import sqlite3

from flask import Flask, g, render_template, request, send_from_directory
from markupsafe import Markup


app = Flask(__name__)


def database():
    if "db" not in g:
        g.db = sqlite3.connect(":memory:")
        g.db.execute("CREATE TABLE users (username TEXT NOT NULL)")
        g.db.executemany(
            "INSERT INTO users (username) VALUES (?)",
            [("ana",), ("luis",)],
        )
    return g.db


@app.teardown_appcontext
def close_database(_error):
    db = g.pop("db", None)
    if db is not None:
        db.close()


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/reporte")
def reporte():
    return send_from_directory("reportes", "semgrep.html")


@app.get("/inseguro/buscar")
def buscar_inseguro():
    name = request.args.get("nombre", "")
    rows = database().execute(
        f"SELECT username FROM users WHERE username = '{name}'"
    ).fetchall()
    return {"usuarios": [row[0] for row in rows]}


@app.get("/seguro/buscar")
def buscar_seguro():
    name = request.args.get("nombre", "")
    rows = database().execute(
        "SELECT username FROM users WHERE username = ?", (name,)
    ).fetchall()
    return {"usuarios": [row[0] for row in rows]}


@app.get("/inseguro/saludo")
def saludo_inseguro():
    name = request.args.get("nombre", "")
    return Markup(f"<h1>Hola, {name}</h1>")


@app.get("/seguro/saludo")
def saludo_seguro():
    name = request.args.get("nombre", "")
    return render_template("saludo.html", name=name)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
