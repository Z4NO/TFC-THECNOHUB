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

    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True
    
    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return self.email
    

    def get(user_id):
        from BaseManager import BaseManager
        basemanager = BaseManager()
        usuario = basemanager._get_user_by_email(user_id)
        if usuario:
            return usuario
        else:
            return None

