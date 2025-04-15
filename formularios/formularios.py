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


formularios = Blueprint('formularios', __name__, url_prefix='/formularios')

@formularios.route('/main', methods=['POST', 'GET'])
def cargar_main():
    return render_template('main.html')

@formularios.route('/especificar', methods=['POST', 'GET'])
def cargar_especificar():
    return render_template('especificar.html')
