import re
from flask import Flask, redirect, request, jsonify,  render_template, url_for
from flask import session
import requests
import secrets
import urllib.parse
from formularios.formularios import formularios as formularios
import datetime
from BaseManager import BaseManager
from Encripter import Encripter
from dotenv import load_dotenv
from User import User
import os
from typing import Final

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Crear la app de Flask
app = Flask(__name__)
# Generar una clave secreta para la app
app.secret_key = secrets.token_hex(16)
app.register_blueprint(formularios)


# Datos de la app de Spotify
MASTER_KEY: Final[str] = os.getenv('MASTER_KEY')


encripter = Encripter(MASTER_KEY.encode())

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
            print(f"Credenciales correctas para el usuario: {email}")
            return redirect(url_for("formularios.cargar_main"))
        else:
            return redirect('/incorrect')

    return render_template('index.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        contrasena = request.form.get('contrasena')
        nombre = request.form.get('nombre')
        preferencias = request.form.getlist('preferencias')
        reputacion = 0
        rol = 'usuario'

        user = User(contrasena, email, nombre, preferencias, reputacion, rol)
        base_manager = BaseManager()

        if base_manager._add_user(user):
            return redirect('/')
        else:
            return redirect('/incorrect')

    return render_template('registro.html')

# Ruta de credenciales incorrectas


@app.route('/incorrect')
def incorrect():
    return render_template("nocredentials.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
