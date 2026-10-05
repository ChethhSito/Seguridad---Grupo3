"""Correcciones de la muestra generada por IA.

Este archivo debe permanecer limpio: el pre-commit y GitHub Actions lo bloquean
si alguna regla del laboratorio vuelve a coincidir.
"""

import hashlib
import json
import logging
import os


AVATARES = {"ana": b"ana", "luis": b"luis"}


def resumen(dato):
    return hashlib.sha256(dato).hexdigest()


def cargar_perfil(contenido):
    return json.loads(contenido)


def arrancar(aplicacion):
    aplicacion.run(host="127.0.0.1", debug=False)


def anotar_acceso():
    logging.info("acceso concedido")


def ver_perfil(perfiles, identificador, dueno):
    if identificador != dueno:
        return None
    return perfiles[identificador]


def buscar(conexion, nombre):
    return conexion.execute(
        "SELECT nombre FROM personas WHERE nombre = ?",
        (nombre,),
    )


def saludar(nombre):
    return nombre


def descargar(nombre):
    return AVATARES.get(nombre, b"")


def entrar(es_admin):
    return bool(es_admin)


def clave_desde_entorno():
    return os.environ["CLAVE_DEMO"]
