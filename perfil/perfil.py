from flask import Flask, redirect, request, jsonify,  render_template, url_for, Blueprint
from flask import session
from flask_login import login_user, login_required, logout_user, current_user
import requests
import secrets
import urllib.parse
import datetime
from BaseManager import BaseManager
from Encripter import Encripter
from dotenv import load_dotenv
from User import User
import os
from typing import Final


perfil = Blueprint('profile', __name__, url_prefix='/profile')
upload_folder = 'static/imgs/'

# Carga el profile


@perfil.route('/main', methods=['POST', 'GET'])
@login_required
def cargar_profile():
    user = User.get(current_user.email)
    print(f"Ruta de la foto de perfil: {current_user.foto_perfil}")
    print(user)

    return render_template('profile.html', user=user)


@perfil.route('/actualizar-foto', methods=['GET'])
@login_required
def actualizar_foto():
    return render_template('actualizar-foto.html')


@perfil.route('/upload_foto_perfil', methods=['POST'])
@login_required
def upload_profile_pic():
    if 'foto_perfil' not in request.files:
        return "No se seleccionó ninguna imagen", 400

    file = request.files['foto_perfil']

    if file.filename == '':
        return "Nombre archivo vacio", 400

    filename = "image.png"
    file_path = os.path.join(upload_folder, filename)
    print(f"Guardando imagen en: {file_path}")
    file.save(file_path)

    current_user.foto_perfil = url_for('static', filename='imgs/' + filename)
    print(current_user.foto_perfil)
    User.update_profile_pic(current_user.email, current_user.foto_perfil)

    return redirect(url_for('profile.cargar_profile'))


@perfil.route('/actualizar-nombre', methods=['POST'])
@login_required
def actualizar_nombre():
    nuevo_nombre = request.form.get('nombre')

    if not nuevo_nombre:
        return 'El nombre no puede estar vacio'

    current_user.nombre = nuevo_nombre
    User.update_name(current_user.email, nuevo_nombre)
    return redirect(url_for('profile.cargar_profile'))


@perfil.route('/actualizar-preferencias', methods=['POST'])
@login_required
def actualizar_preferencias():
    preferencias = request.form.getlist("preferencias")

    if not preferencias:
        return "Las preferencias no pueden estar vacías", 400

    current_user.preferencias = preferencias
    User.update_preferences(current_user.email, preferencias)

    return redirect(url_for('profile.cargar_profile'))
