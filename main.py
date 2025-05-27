from datetime import datetime, timezone, timedelta
from flask import Flask, redirect, request, jsonify,  render_template, url_for
from flask import session
from flask_login import LoginManager, login_user, login_required, current_user
from formularios.formularios import foro as foro
from perfil.perfil import perfil as perfil
from urllib.parse import unquote
from mensajes.mensajes import mensajes as mensajes
from BaseManager import BaseManager
from Encripter import Encripter
from dotenv import load_dotenv
from User import User
import os
from extension import socketio
from typing import Final
from algoritmos import *
from formularios.formularios import ForoModel
from flask_caching import Cache


# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Datos de la app de Spotify
MASTER_KEY: Final[str] = os.getenv('MASTER_KEY')


# Crear la app de Flask
app = Flask(__name__)
# Generar una clave secreta para la app
app.secret_key = MASTER_KEY

# variables de entorno / configuracion de la app
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'
app.register_blueprint(foro)
app.register_blueprint(perfil)
app.register_blueprint(mensajes)

# configuramos el socketio
socketio.init_app(app, cors_allowed_origins="*")


encripter = Encripter(MASTER_KEY.encode())
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# Rutas del login_namager


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


# Rutas de la app
"""
Handles the index route for the web application.
This function processes both GET and POST requests to the root URL ('/'). 
For POST requests, it checks if the user is logged in using the provided ID. 
If the user is not logged in, it retrieves the ID and Key from the form data, 
validates the credentials, and sets the session variables if the credentials are valid. 
If the credentials are invalid, it redirects to the '/incorrect' page. 
For GET requests, it renders the 'index.html' template.
Returns:
    Response: A redirect to the 'login' route with the user's ID and Key if the credentials are valid.
    Response: A redirect to the '/incorrect' page if the credentials are invalid.
    Response: Renders the 'index.html' template for GET requests.
"""


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        email = request.form.get('email')
        contrasena = request.form.get('contrasena')
        print(f"Email: {email}, Contrasena: {contrasena}")

        base_manager = BaseManager()
        if base_manager._check_credentials(email, contrasena):
            session['email'] = email
            session['contrasena'] = contrasena
            login_user(User.get(email))

            return redirect('/index')
        else:
            return redirect('/incorrect')

    return render_template('index.html')


@app.route('/index', methods=['POST', 'GET'])
@login_required
def index2():
    valor = unquote(request.args.get("valor", ""))
    perfiles_list = get_users_by_preferences(User.get(current_user.email))
    foros_lista = basemanager.get_forums_without_messages()
    foros_usuario = basemanager.get_foros_by_user(
        User.get(current_user.nickname))
    perfiles_busqueda = []
    foros_busqueda = []
    usuario_buscado = None
    print(f"resultado valor: {valor}")
    if valor:
        resultados = basemanager.get_data_by_field(valor)
        print("Resultados obtenidos:", resultados)
        perfiles_busqueda = resultados["usuarios"]
        foros_busqueda = resultados["foros"]
        if perfiles_busqueda:
            usuario_buscado = basemanager.get_user_by_nickname(
                perfiles_busqueda[0].nickname)

    foros_encontrados = [{'dueñonombre': foro.dueñonombre, 'dueño_nickname': f"@{foro.dueño_nickname}", 'Descripcion': foro.descripcion,
                          'Likes': foro.likes, 'Comentarios': foro.comentarios, 'titulo': foro.titulo, 'foro': foro} for foro in foros_busqueda]
    perfiles_encontrados = [
        {'nombre': perfil.nombre, 'nickname': perfil.nickname, 'foto_perfil': perfil.foto_perfil, 'fecha_creacion': perfil.fecha_creacion} for perfil in perfiles_busqueda]

    foros = []
    for foro in foros_lista if len(perfiles_list) >= 1 else []:
        foros.append(
            {'Nombre':foro.titulo,'dueñonombre': foro.dueñonombre, 'dueño_nickname': f"@{foro.dueño_nickname}", 'Descripcion': foro.descripcion, 'Likes': foro.likes, 'Comentarios': foro.comentarios, 'titulo': foro.titulo, 'id': foro.id,'dueño': foro.dueño ,'foro': foro})

    foros_usuarios = []
    for foro in foros_usuario if len(perfiles_list) >= 1 else []:
        foros_usuarios.append(
            {'dueñonombre': foro.dueñonombre, 'dueño_nickname': f"@{foro.dueño_nickname}", 'Descripcion': foro.descripcion, 'Likes': foro.likes, 'Comentarios': foro.comentarios, 'titulo': foro.titulo, 'foro': foro})

    perfiles = [
    ]
    # vamos a recorrer los perfiles y a añadirlos a la lista de perfiles
    for perfil in perfiles_list if len(perfiles_list) >= 1 else []:
        perfiles.append(
            {'nombre': perfil.nombre, 'usuario': f"@{perfil.nickname}"})

    tendencias = [
        {'titulo': 'WananPagaCrunchyroll', 'publicaciones': '1'},
        {'titulo': 'CurroGym', 'publicaciones': '124'},
        {'titulo': 'ExplotanMedac', 'publicaciones': '234k'}
    ]

    post_recomendados = [
        {'Usuario': 'Bando002', 'Nickname': '@usuario1',
            'Contenido': 'HTML5 y CSS es el futuro de la maquetacion de web'},
        {'Usuario': 'Dani', 'Nickname': '@usuario2',
            'Contenido': 'La informatica es el futuro, la programacion es el destino'},
        {'Usuario': 'Wanan', 'Nickname': '@LilWanan',
            'Contenido': 'SQL no es tan complicado si te pones todos los dias'}
    ]
    print(f"foro de cada usuario: {foros_usuarios}")

    return render_template('main.jinja', perfiles=perfiles, tendencias=tendencias, post_recomendados=post_recomendados, foros=foros, foros_encontrados=foros_encontrados, perfiles_encontrados=perfiles_encontrados, usuario_buscado=usuario_buscado, foros_usuarios=foros_usuarios)


@app.route('/index/endpoint', methods=['POST'])
@login_required
def index_endpoint():
    # En esta ruta vamos a manejar lso datos que nos envian desde el frontend
    print("Index endpoint")


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        contrasena = request.form.get('contrasena')
        nombre = request.form.get('nombre')
        preferencias = request.form.getlist('preferencias')
        reputacion = 0
        rol = 'usuario'
        nickname = request.form.get('nickname')

        user = User(contrasena=contrasena, email=email, nickname=nickname,
                    nombre=nombre, preferencias=preferencias, reputacion=reputacion, rol=rol)
        base_manager = BaseManager()

        if base_manager._add_user(user):
            return redirect('/')
        else:
            return redirect('/incorrect')

    return render_template('registro.html')

# Ruta de credenciales incorrectas


# @app.route("/buscar", methods=["GET"])
# @login_required
# def buscar():
#     valor = unquote(request.args.get("valor", ""))
#     if not valor:
#         return jsonify({"usuarios": [], "posts": []})

#     resultados = basemanager.get_data_by_field(valor)
#     print(f"Resultados obtenidos: {resultados}")

#     return jsonify(resultados)

@app.route("/buscar", methods=["GET"])
@login_required
def buscar():
    valor = unquote(request.args.get("valor", ""))
    if not valor:
        return jsonify({"usuarios": [], "foros": []})

    resultados = basemanager.get_data_by_field(valor)

    # Convertir los objetos en diccionarios antes de enviarlos como JSON
    usuarios_data = [user.__dict__ for user in resultados["usuarios"]]
    foros_data = [foro.__dict__ for foro in resultados["foros"]]

    return jsonify({"usuarios": usuarios_data, "foros": foros_data})


# @app.route('/popup')
# def popup():
#     return render_template('components/popuppost.html')

@app.route('/popup')
def popup():
    return render_template('popupcrearforo.html')


@app.route('/postear', methods=['POST'])
def postear():
    try:
        titulo = request.form.get('titulo')
        descripcion = request.form.get('descripcion')
        categorias = request.form.getlist('categorias')
        user = User.get(current_user.email)

        foro = ForoModel(
            titulo=titulo,
            descripcion=descripcion,
            dueño=user.email,
            categorias=categorias,
        )
        resultado = basemanager._add_forum(user, foro)
        print(f"Resultado de _add_forum(): {resultado}")

        if not resultado or resultado is False:
            return jsonify({"message": "Error al crear el foro, pero sí se guardó en Firebase"}), 500

        return jsonify({"message": "Foro creado exitosamente"}), 200

    except Exception as e:
        print(f"Error en postear(): {str(e)}")
        return jsonify({"message": f"Error: {str(e)}"}), 500


@app.route('/incorrect')
def incorrect():
    return render_template("nocredentials.html")


if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
