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
from urllib.parse import quote, unquote
from typing import List, Optional


foro = Blueprint('foro', __name__, url_prefix='/foro')


class ForoModel:
    def __init__(
        self,
        descripcion: str,
        dueño: str,
        titulo: str,
        categorias: List[str],
        fecha_creacion: datetime = datetime.now(timezone.utc),
        likes: int = 0,
        comentarios: int = 0,
        fecha_finalizacion: Optional[datetime] = None,
        fecha_modificado: Optional[datetime] = None,
        dueñonombre: Optional[str] = None,
        dueño_nickname: Optional[str] = None,
        mensajes: Optional[List[dict]] = None
    ):
        self.likes = likes
        self.comentarios = comentarios
        self.descripcion = descripcion
        self.dueño = dueño
        self.titulo = titulo
        self.categorias = categorias
        self.fecha_creacion = fecha_creacion
        self.fecha_finalizacion = fecha_finalizacion
        self.fecha_modificado = fecha_modificado
        self.dueñonombre = dueñonombre
        self.dueño_nickname = dueño_nickname
        self.mensajes = mensajes if mensajes is not None else []




# carga foro con el html que todavia no esta creado y le pasa el current_user.preferencias


@foro.route('/main', methods=['POST', 'GET'])
@login_required
def cargar_foro():
    forodescripcion = unquote(request.args.get('forodescripcion'))
    forodueño = unquote(request.args.get('forodueño'))
    forotitulo = unquote(request.args.get('forotitulo'))
    return render_template('foro.jinja', 
                           forodescripcion=forodescripcion,
                           forodueño=forodueño,
                           forotitulo=forotitulo,
                           current_user=current_user)


# @foro.route('/')
# def index():
#     return render_template('index.html')
