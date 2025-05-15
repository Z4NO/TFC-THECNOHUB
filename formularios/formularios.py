from flask import Flask, redirect, request, jsonify,  render_template, url_for, Blueprint
from flask import session
from flask_login import *
import requests
import secrets
import urllib.parse
from datetime import datetime, timezone
from Encripter import Encripter
from dotenv import load_dotenv
from User import User
import os
from typing import Final


foro = Blueprint('foro', __name__, url_prefix='/foro')


class ForoModel:
    def __init__(
        self,
        descripcion: str,
        dueño: str,
        titulo: str,
        categorias: list,
        fecha_creacion: datetime = datetime.now(timezone.utc),
        fecha_finalización: datetime = None,
        fecha_modificado: datetime = None
    ):
        self.descripcion = descripcion
        self.dueño = dueño
        self.titulo = titulo
        self.categorias = categorias
        self.fecha_creacion = fecha_creacion
        self.fecha_finalizacion = fecha_finalización
        self.fecha_modificado = fecha_modificado
        self.mensajes = []





# carga foro con el html que todavia no esta creado y le pasa el current_user.preferencias


@foro.route('/main', methods=['POST', 'GET'])
def cargar_foro():
    foro = ForoModel.get(categorias=User.get(current_user.preferencias))
    return render_template('foro.html', foro=foro)


# @foro.route('/')
# def index():
#     return render_template('index.html')
