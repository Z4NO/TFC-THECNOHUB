import re
from flask import Flask, redirect, request, jsonify,  render_template, url_for
from flask import session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import requests
import secrets
import urllib.parse
from formularios.formularios import foro as foro
from perfil.perfil import perfil as perfil
from mensajes.mensajes import mensajes as mensajes
import datetime
from BaseManager import BaseManager
from Encripter import Encripter
from dotenv import load_dotenv
from User import User
import os
from typing import Final
from algoritmos import *

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Crear la app de Flask
app = Flask(__name__)
# Generar una clave secreta para la app
app.secret_key = secrets.token_hex(16)

# variables de entorno / configuracion de la app
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'
app.register_blueprint(foro)
app.register_blueprint(perfil)
app.register_blueprint(mensajes)


# Datos de la app de Spotify
MASTER_KEY: Final[str] = os.getenv('MASTER_KEY')


encripter = Encripter(MASTER_KEY.encode())


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
    perfiles_list = get_users_by_preferences(User.get(current_user.email))
    print(f"Perfiles: {perfiles_list}")
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
            'Contenido': 'Contenido del post 1'},
        {'Usuario': 'Dani', 'Nickname': '@usuario2',
            'Contenido': 'Contenido del post 2'},
        {'Usuario': 'Wanan', 'Nickname': '@LilWanan',
            'Contenido': 'Lo de trabajar para gastarlo todo en 1 semana es loco, no puedo hacer mas de 12 viajes al mes, estoy cansado.#FrikingPagaMas #PonedAireEnFriking '}
    ]

    return render_template('main.jinja', perfiles=perfiles, tendencias=tendencias, post_recomendados=post_recomendados)


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


@app.route('/incorrect')
@login_required
def incorrect():
    return render_template("nocredentials.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
