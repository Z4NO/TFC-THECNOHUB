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


basemanager = BaseManager()


# Vamos a hacer que te devuelva los usuarios los cuales tengan los mismos gustos / preferencias que el usuario que ha iniciado sesion,
# para ello vamos a utilizar el metodo de la base de datos que nos devuelve los usuarios por preferencias además del de filftrar por el campo que queramos(algoritmo de busqueda).,

def get_users_by_preferences(user: User) -> list:
    # Obtenemos las preferencias del usuario que ha iniciado sesion
    user_preferences = user.preferencias
    # Obtenemos los usuarios que tienen las mismas preferencias que el usuario que ha iniciado sesion
    users = basemanager._get_users_by_algorithm(
        user_preferences, 'preferencias', user.email)
    return users

