from flask import Flask, redirect, request, jsonify,  render_template, url_for, Blueprint, send_from_directory
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
    dias_creacion = user.antiguedad_cuenta() if user.fecha_creacion else 0

    return render_template('profile.html', user=user, dias_creacion=dias_creacion)


@perfil.route('/main/<usuario>', methods=['GET'])
@login_required
def cargar_profile_by_search(usuario):

    perfil = User.get_by_nickname(usuario)

    dias_creacion = perfil.antiguedad_cuenta() if perfil.fecha_creacion else 0
    return render_template('profile.html', user=perfil, dias_creacion=dias_creacion)


@perfil.route('/actualizar-foto', methods=['GET'])
@login_required
def actualizar_foto():
    return render_template('actualizar-foto.html')


@perfil.route('/')
def index():
    return render_template('index.html')


@perfil.route('/upload_foto_perfil', methods=['POST'])
@login_required
def upload_profile_pic():
    if 'foto_perfil' not in request.files:
        return "No se seleccionó ninguna imagen", 400

    file = request.files['foto_perfil']

    if file.filename == '':
        return "Nombre archivo vacio", 400

    filename = f"{current_user.email}.png"
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


@perfil.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('index'))


@perfil.route('/actualizar-suscripcion', methods=['POST'])
@login_required
def actualizar_suscripcion():
    nuevo_estado = request.form.get("suscripcion", "premium")
    dias_validos = int(request.form.get("fecha_expiracion_premium", 30))

    if not nuevo_estado:
        return jsonify({"error": "El estado de la suscripción no puede estar vacío"}), 400

    resultado = User.update_subscription_with_expiration(
        current_user.email, nuevo_estado, dias_validos)

    if resultado:
        return redirect(url_for('profile.cargar_profile'))
    else:
        return jsonify({"error": "No se pudo actualizar la suscripción"}), 500


@perfil.route('/opciones-ajustes', methods=['GET'])
@login_required
def opciones_ajustes():
    return render_template("opciones-ajustes.html")
