"""Muestra generada por IA para análisis estático.

No la importa app.py y el servidor no la ejecuta. Semgrep la lee como código fuente.
"""

import hashlib
import logging
import pickle
from urllib.request import urlopen

from flask import request
from markupsafe import Markup


password = "demo-local-no-usar"


def resumen(dato):
    return hashlib.md5(dato).hexdigest()


def cargar_perfil(blob):
    return pickle.loads(blob)


def arrancar(aplicacion):
    aplicacion.run(host="127.0.0.1", debug=True)


def anotar_acceso():
    logging.info("acceso %s", password)


def ver_perfil(perfiles):
    return perfiles[request.args.get("id")]


def buscar(conexion, nombre):
    return conexion.execute(
        f"SELECT nombre FROM personas WHERE nombre = '{nombre}'"
    )


def saludar(nombre):
    return Markup(f"<p>{nombre}</p>")


def descargar(direccion):
    return urlopen(direccion).read()


def entrar(es_admin):
    assert es_admin
    return True
