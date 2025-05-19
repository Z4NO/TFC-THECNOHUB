import datetime
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore import FieldFilter
from datetime import datetime, timezone, timedelta
import os


class User:
    def __init__(
        self,
        contrasena: str,
        email: str,
        nickname: str,
        nombre: str,
        preferencias,
        reputacion,
        rol: str,
        foto_perfil: str = "static/imgs/pa.webp",
        fecha_creacion: datetime = datetime.now(timezone.utc),
        suscripcion: str = "basico",
        fecha_expiracion_premium: datetime = None
    ):
        self.contrasena = contrasena
        self.email = email
        self.nombre = nombre
        self.preferencias = preferencias
        self.reputacion = reputacion
        self.rol = rol
        self.foto_perfil = foto_perfil
        self.nickname = nickname
        self.fecha_creacion = fecha_creacion
        self.suscripcion = suscripcion
        self.fecha_expiracion_premium = fecha_expiracion_premium if fecha_expiracion_premium else None

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

    def antiguedad_cuenta(self):
        hoy = datetime.now(timezone.utc)
        diferencia = hoy - self.fecha_creacion
        return diferencia.days

    def update_profile_pic(user_id, new_pic_url):
        db = firestore.client()
        query = db.collection("usuario").where(
            "email", "==", user_id).limit(1).get()

        if not query:
            print(f"Error: El usuario {user_id} no existe en Firestore.")
            return False

        user_ref = query[0].reference
        user_ref.update({"foto_perfil": new_pic_url})
        print(f"Foto de perfil actualizada: {new_pic_url}")
        return True

    def update_name(user_id, new_name):
        db = firestore.client()
        query = db.collection("usuario").where(
            "email", "==", user_id).limit(1).get()

        if not query:
            print(f"Error: El usuario {user_id} no existe en Firestore.")
            return False

        user_ref = query[0].reference

        user_ref.update({"nombre": new_name})

        print(f"Nombre actualizado: {new_name}")
        return True

    def update_preferences(user_id, preferencias):
        db = firestore.client()
        query = db.collection("usuario").where(
            "email", "==", user_id).limit(1).get()

        if not query:
            print(f"Error: El usuario {user_id} no existe en Firestore.")
            return False

        user_ref = query[0].reference  # Obtener referencia del usuario
        # Actualizar preferencias
        user_ref.update({"preferencias": preferencias})

        print(f"Preferencias actualizadas para {user_id}: {preferencias}")
        return True

    def update_subscription_with_expiration(user_id, new_status="premium", days_valid=30):
        db = firestore.client()
        query = db.collection("usuario").where(
            "email", "==", user_id).limit(1).get()

        if not query:
            print(f"Error: El usuario {user_id} no existe en Firestore.")
            return False

        user_ref = query[0].reference
        expiration_date = datetime.now() + timedelta(days=days_valid)

        user_ref.update({
            "suscripcion": new_status,
            "fecha_expiracion_premium": expiration_date
        })

        print(
            f"Suscripción actualizada para {user_id}: {new_status}, expira el {expiration_date}")
        return True
