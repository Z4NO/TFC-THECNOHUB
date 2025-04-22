import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore import FieldFilter
import datetime
from User import User
from Encripter import Encripter
import os


class BaseManager:
    def __init__(self):
        try:
            self.cred = credentials.Certificate(os.path.join(os.path.dirname(
                __file__), "tfgforo-firebase-adminsdk-fbsvc-61fd334c13.json"))
            self.encripter = Encripter(os.getenv('MASTER_KEY').encode())
            if not firebase_admin._apps:
                firebase_admin.initialize_app(self.cred)
            self.db = firestore.client()
            self.encripter = Encripter(os.getenv('MASTER_KEY').encode())
        except Exception as e:
            print(f"Error al iniciar la base de datos: {e}")
            self.db = None


    def _add_user(self, user: User):
        try:
            if self._email_exists(user.email):
                print("El email ya esta registrado")
                return False
            # Crear un nuevo documento en la colección 'users'
            self.db.collection('usuario').add({
                'contrasena': self.encripter._encript(user.contrasena),
                'email': user.email,
                'nombre': user.nombre,
                'preferencias': user.preferencias,
                'reputacion': user.reputacion,
                'rol': user.rol
            })
            return True
        except Exception as e:
            print(f"Error al añadir el usuario: {e}")
            return False
        


    def _check_credentials(self, email, password) -> bool:
        try:
            user_ref = self.db.collection('usuario')
            user_ref_query = user_ref.where('email', '==', email).stream()
            # traemos la contrasena encriptada de la base de datos y la desencriptamos para compararla
            for doc in user_ref_query:
                user_data = doc.to_dict()
                contraseña_desencriptada = self.encripter._decript(
                    user_data['contrasena'])
                break
            if contraseña_desencriptada == password:
                return True
            else:
                return False
        except Exception as e:
            print(f"Error al verificar las credenciales: {e}")
            return False


    def _email_exists(self, email: str) -> bool:
        try:
            user_ref = self.db.collection('usuario')
            user_ref_query = user_ref.where('email', '==', email).stream()
            for doc in user_ref_query:
                if doc:
                    return True
            return False
        except Exception as e:
            print(f"Error al comprobar si el email existe: {e}")
            return False
        

    def _get_user_by_email(self, email: str) -> User:
        try:
            user_ref = self.db.collection('usuario')
            user_ref_query = user_ref.where('email', '==', email).stream()
            for doc in user_ref_query:
                user_data = doc.to_dict()
                return User(
                    contrasena=self.encripter._decript(user_data['contrasena']),
                    email=user_data['email'],
                    nombre=user_data['nombre'],
                    preferencias=user_data['preferencias'],
                    reputacion=user_data['reputacion'],
                    rol=user_data['rol']
                )
            return None
        except Exception as e:
            print(f"Error al obtener el usuario por email: {e}")
            return None
