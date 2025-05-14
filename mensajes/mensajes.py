import json
from flask import Flask, redirect, request, jsonify,  render_template, url_for, Blueprint
from flask import session 
from flask_socketio import  join_room, leave_room
from flask_login import login_required, current_user
from dotenv import load_dotenv
from User import User
from extension import socketio 
from flask import request
from BaseManager import BaseManager
from md import md as MD


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



# Vamos a manejar las rooms en socketio para qu los usuarios solo se puedan coenectar a su sala
# Esto lo vamos a hacer de la siguiente manera:
# 1. las salas las vamos a extaer de la base de datos para saver cuales son los dos ids (emails) de los usuarios que se van a conectar
# 2. Vamos a comprobar que el current_user se pueda conectar a la sala a través de su id (email)
# 3. Si el current_user se puede conectar a la sala vamos a añadirlo a la sala
# 4. Si el current_user no se puede conectar a la sala vamos a devolver un error , muy importante no conectarse a la sala hasta  que se haya comprobado que el current_user se puede conectar a la sala


def obtener_md(email: str) -> MD:
    lista_users = [current_user.email, email]
    try:
        md = BaseManager._get_private_md(lista_users=lista_users)
        return md
    except Exception as e:
        print(f"Error al obtener el md: {e}")
        return None
    

@socketio.on('join', namespace='/main/mensajes')
def handle_join(data):
    room = data.get('room')
    join_room(room)
    print(f'➡️ Usuario {current_user.email} se ha unido a la sala: {room}')
    socketio.emit('status', {'msg': f'Usuario {current_user.email} se ha unido a la sala: {room}'}, to=room, namespace='/main/mensajes', skip_sid=request.sid)


@socketio.on('leave', namespace='/main/mensajes')
def handle_leave(data):
    room = data.get('room')
    if room:
        leave_room(room)
        print(f'⬅️ {current_user.email} ha salido de {room}')



@socketio.on('connect', namespace='/main/mensajes')
def handle_connect():
    print(F'➡️ Cliente conectado al namespace /mensajes{User.get(current_user.email).nickname}')

@socketio.on('disconnect', namespace='/main/mensajes')
def handle_disconnect():
    print('❌ Cliente desconectado del namespace /mensajes')

@socketio.on('send_mensaje', namespace='/main/mensajes')
def handle_mensaje(data):
    print(f"💬 Mensaje recibido: {data.get('msg')} en la sala {data.get('room')}")
    socketio.emit('respuesta', {'msg': data.get('msg')}, namespace='/main/mensajes', skip_sid=request.sid, to=data.get('room'))

@socketio.on('respuesta', namespace='/main/mensajes')
def handle_respuesta(data):
    print(f'💬 Respuesta recibida: {data.get('msg')}')
    socketio.emit('respuesta', {'response': 'Respuesta recibida'}, namespace='/main/mensajes' , skip_sid=request.sid, to=data.get('room'))