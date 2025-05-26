from flask import Flask, redirect, request, jsonify,  render_template, url_for, Blueprint
from flask import session
from flask_login import *
from datetime import datetime, timezone
from Encripter import Encripter
from dotenv import load_dotenv
from urllib.parse import quote, unquote
from typing import List, Optional
from extension import get_messages


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
        mensajes: Optional[List[dict]] = None,
        id: str = None,
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
        self.id = id




# carga foro con el html que todavia no esta creado y le pasa el current_user.preferencias


@foro.route('/main', methods=['POST', 'GET'])
@login_required
def cargar_foro():
    forodescripcion = unquote(request.args.get('forodescripcion'))
    forodueño = unquote(request.args.get('forodueño'))
    forotitulo = unquote(request.args.get('forotitulo'))
    foroid = unquote(request.args.get('foroid'))
    #vamos a cargar los mensajes del foro
    mensajes = get_messages(foroid)
    print(f"Mensajes obtenidos: {mensajes}")
    mensajes_list = []
    for mensaje in mensajes:
        mensajes_list.append({
            'fecha': mensaje['fecha'],
            'contenido': mensaje['contenido'],
            'autor': mensaje['autor']
        })

    return render_template('foro.jinja', 
                           forodescripcion=forodescripcion,
                           forodueño=forodueño,
                           forotitulo=forotitulo,
                           current_user=current_user,
                           mensajes=mensajes_list,)


# @foro.route('/')
# def index():
#     return render_template('index.html')
