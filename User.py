import datetime
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore import FieldFilter
import datetime
import os

class User:
    def __init__(
            self, 
            contrasena : str,
            email: str,
            nombre: str,
            preferencias,
            reputacion ,
            rol: str
        ):
        self.contrasena = contrasena
        self.email = email
        self.nombre = nombre
        self.preferencias = preferencias
        self.reputacion = reputacion
        self.rol = rol

