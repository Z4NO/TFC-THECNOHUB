import json
from flask import Flask, redirect, request, jsonify,  render_template, url_for, Blueprint
from flask import session
from flask_login import login_required, current_user
from dotenv import load_dotenv
from User import User
from extension import socketio 
from flask import request


mensajes = Blueprint('mensajes', __name__, url_prefix='/mensajes')



# @formularios.route('/profile', methods=['POST', 'GET']) lo comento pero esto seria curioso usarlo para recuperar la contraseña en caso que se olvide
# def cargar_profile():
#     return render_template('profile.html')

# Carga el profile
@mensajes.route('/main/mensajes', methods=['POST', 'GET'])
@login_required
def cargar_mensajes():
    #vamos a conectar el socketio para comprobar si el usuario se puede conectar
    return render_template('main_mensajes.jinja')


@socketio.on('connect', namespace='/main/mensajes')
def handle_connect():
    print(F'➡️ Cliente conectado al namespace /mensajes{User.get(current_user.email).nickname}')

@socketio.on('disconnect', namespace='/main/mensajes')
def handle_disconnect():
    print('❌ Cliente desconectado del namespace /mensajes')

@socketio.on('send_mensaje', namespace='/main/mensajes')
def handle_mensaje(data):
    print(f'💬 Mensaje recibido: {data}')
    # Aquí puedes procesar el mensaje y enviar una respuesta si es necesario
    socketio.emit('respuesta', {'msg': data['msg']}, namespace='/main/mensajes', skip_sid=request.sid)

@socketio.on('respuesta', namespace='/main/mensajes')
def handle_respuesta(data):
    print(f'💬 Respuesta recibida: {data}')
    socketio.emit('respuesta', {'response': 'Respuesta recibida'}, namespace='/main/mensajes')