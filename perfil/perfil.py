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


perfil = Blueprint('profile', __name__, url_prefix='/profile')

# Carga el profile
@perfil.route('/main', methods=['POST', 'GET'])
def cargar_profile():
    return render_template('profile.html')

