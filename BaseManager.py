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
            self.cred = credentials.Certificate(os.path.join(os.path.dirname(__file__), "tfgforo-firebase-adminsdk-fbsvc-61fd334c13.json"))
            self.encripter =  Encripter(os.getenv('MASTER_KEY').encode())
            if not firebase_admin._apps:
                firebase_admin.initialize_app(self.cred)
            self.db = firestore.client()
            self.encripter = Encripter(os.getenv('MASTER_KEY').encode())
        except Exception as e:
            print(f"Error al iniciar la base de datos: {e}")
            self.db = None

    def _add_user(self, user: User):
        try:
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

    def _check_credentials(self,email, password):
        try:
            # Buscar el usuario en la base de datos
            user_ref = self.db.collection('usuario').where('email', '==', email).get()
            if user_ref:
                for user in user_ref:
                    if user.to_dict().get('contrasena') == self.encripter._encript(password):
                        return True
                return True
            else:
                print(self.encripter._encript(password))
                return False
        except Exception as e:
            print(f"Error al verificar las credenciales: {e}")
            return False