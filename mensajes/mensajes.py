from flask import Flask, redirect, request, jsonify,  render_template, url_for, Blueprint
from flask import session
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


mensajes = Blueprint('mensajes', __name__, url_prefix='/mensajes')


@mensajes.route('/main', methods=['POST', 'GET'])
def cargar_main():
    return render_template('main.html')


# @formularios.route('/profile', methods=['POST', 'GET']) lo comento pero esto seria curioso usarlo para recuperar la contraseña en caso que se olvide
# def cargar_profile():
#     return render_template('profile.html')

# Carga el profile
@mensajes.route('/main/profile', methods=['POST', 'GET'])
def cargar_profile():
    return render_template('profile.html')
