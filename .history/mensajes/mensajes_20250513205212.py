from flask import Flask, redirect, request, jsonify,  render_template, url_for, Blueprint
from flask import session
from flask_login import login_required
from dotenv import load_dotenv
from User import User
from extension import socketio 


mensajes = Blueprint('mensajes', __name__, url_prefix='/mensajes')



# @formularios.route('/profile', methods=['POST', 'GET']) lo comento pero esto seria curioso usarlo para recuperar la contraseña en caso que se olvide
# def cargar_profile():
#     return render_template('profile.html')

# Carga el profile
@mensajes.route('/main/mensajes', methods=['POST', 'GET'])
@login_required
def cargar_mensajes():
    #vamos a conectar el socketio para comprobar si el usuario se puede conectar
    if socketio is not None:
        print('SocketIO está disponible')
        print(type(socketio))
    return render_template('main_mensajes.jinja')


@socketio.on('connect', namespace='/mensajes')
def handle_connect():
    print('Usuario conectado al namespace /mensajes')