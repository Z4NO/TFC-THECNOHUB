import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore import FieldFilter
import datetime
from User import User
from Encripter import Encripter
import os

from formularios.formularios import ForoModel, MensajeForo


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
                'foto_perfil': user.foto_perfil,
                'rol': user.rol,
                'nickname': user.nickname,
                'fecha_creacion': user.fecha_creacion,
                'suscripcion': user.suscripcion,
                'fecha_expiracion_premium': user.fecha_expiracion_premium
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
                    contrasena=self.encripter._decript(
                        user_data['contrasena']),
                    email=user_data['email'],
                    nombre=user_data['nombre'],
                    preferencias=user_data['preferencias'],
                    reputacion=user_data['reputacion'],
                    rol=user_data['rol'],
                    foto_perfil=user_data['foto_perfil'],
                    nickname=user_data['nickname'],
                    fecha_creacion=user_data['fecha_creacion'],
                    suscripcion=user_data['suscripcion'],
                    fecha_expiracion_premium=user_data['fecha_expiracion_premium']
                )
            return None
        except Exception as e:
            print(f"Error al obtener el usuario por email: {e}")
            return None

    # Vamos a hacer una función la cual toma un número n de usuarios que quiere devolver y una QUERY por la cual filtrar los usuarios, además de un campo por el que filtrar, para facilitar los algoritmos de búsqueda.
    def _get_users_by_algorithm(self, query,  field: str, limit: int = 3) -> list[User]:
        try:
            user_ref = self.db.collection('usuario')

            # Si query es una lista, usamos el operador 'in' para filtrar por múltiples valores
            if isinstance(query, list):
                user_ref_query = user_ref.where(
                    field, 'in', [query]).limit(limit).stream()
            else:
                user_ref_query = user_ref.where(
                    field, '==', query).limit(limit).stream()

            users = []
            for doc in user_ref_query:
                user_data = doc.to_dict()
                users.append(User(
                    contrasena=self.encripter._decript(
                        user_data['contrasena']),
                    email=user_data['email'],
                    nombre=user_data['nombre'],
                    preferencias=user_data['preferencias'],
                    reputacion=user_data['reputacion'],
                    rol=user_data['rol'],
                    foto_perfil=user_data['foto_perfil'],
                    nickname=user_data['nickname'],
                    fecha_creacion=user_data['fecha_creacion'],
                    suscripcion=user_data['suscripcion'],
                    fecha_expiracion_premium=user_data['fecha_expiracion_premium']
                ))
            return users
        except Exception as e:
            print(f"Error al obtener los usuarios por algoritmo: {e}")
            return []


# Foro

    def _add_forum(self, user: User, foro: ForoModel):
        try:

            # Crear un nuevo documento en la colección 'foro'
            self.db.collection('foro').add({
                'Descripcion': foro.descripcion,
                'Dueño': user.email,
                'Tútulo': foro.titulo,
                'categorias': foro.categorias,
                'fecha_creacion': foro.fecha_creacion,
                'fecha_finalizacion': foro.fecha_finalizacion,
                'fecha_modificado': foro.fecha_modificado,
                'mensajes_foro': foro.mensajes
            })
            return True
        except Exception as e:
            print(f"Error al añadir el usuario: {e}")
            return False

    def _get_forum_by_preferences(self, categorias: list) -> list[ForoModel]:
        try:
            foro_ref = self.db.collection('foro')
            foro_ref_query = foro_ref.where(
                'categorias', 'array_contains', categorias).stream()

            foros = []
            for doc in foro_ref_query:
                foro_data = doc.to_dict()

                mensajes_foro = []
                if 'mensajes_foro' in foro_data:
                    for mensaje in foro_data['mensajes_foro']:
                        mensajes_foro.append(MensajeForo(
                            dueño=mensaje['Dueño'],
                            mensaje=mensaje['mensaje']
                        ))

                foros.append(ForoModel(
                    descripcion=foro_data['Descripcion'],
                    dueño=foro_data['Dueño'],
                    titulo=foro_data['Titulo'],
                    categorias=foro_data['categorias'],
                    fecha_creacion=foro_data['fecha_creacion'],
                    fecha_finalizacion=foro_data['fecha_finalizacion'],
                    fecha_modificado=foro_data['fecha_modificado'],
                    mensajes=mensajes_foro
                ))

            return foros

        except Exception as e:
            print(f"Error al obtener los foros por preferencias: {e}")
            return []

    def _get_forums_by_owner(self, email_dueño: str) -> list[ForoModel]:
        try:
            foro_ref = self.db.collection('foro')
            foro_ref_query = foro_ref.where(
                'Dueño', '==', email_dueño).stream()

            foros = []
            for doc in foro_ref_query:
                foro_data = doc.to_dict()

                mensajes_foro = [MensajeForo(
                    m['Dueño'], m['mensaje']) for m in foro_data.get('mensajes_foro', [])]

                foros.append(ForoModel(
                    descripcion=foro_data['Descripcion'],
                    dueño=foro_data['Dueño'],
                    titulo=foro_data['Titulo'],
                    categorias=foro_data['categorias'],
                    fecha_creacion=foro_data['fecha_creacion'],
                    fecha_finalizacion=foro_data.get('fecha_finalizacion'),
                    fecha_modificado=foro_data.get('fecha_modificado'),
                    mensajes=mensajes_foro
                ))

            return foros

        except Exception as e:
            print(f"Error al obtener los foros por dueño: {e}")
            return []
