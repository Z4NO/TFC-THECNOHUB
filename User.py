import datetime
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore import FieldFilter
import datetime
import os


class User:
    def __init__(
        self,
        contrasena: str,
        email: str,
        nombre: str,
        preferencias,
        reputacion,
        rol: str,
        foto_perfil: str = ""
    ):
        self.contrasena = contrasena
        self.email = email
        self.nombre = nombre
        self.preferencias = preferencias
        self.reputacion = reputacion
        self.rol = rol
        self.foto_perfil = foto_perfil

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

    def update_profile_pic(user_id, new_pic_url):
        db = firestore.client()
        query = db.collection("usuario").where(
            "email", "==", user_id).limit(1).get()

        if not query:
            print(f"Error: El usuario {user_id} no existe en Firestore.")
            return False

        user_ref = query[0].reference  # Obtenemos la referencia correcta
        user_ref.update({"foto_perfil": new_pic_url})  # Actualizamos el campo
        print(f"Foto de perfil actualizada: {new_pic_url}")
        return True
