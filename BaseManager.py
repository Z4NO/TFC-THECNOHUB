from typing import Final
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore import FieldFilter
import datetime
from User import User
from Encripter import Encripter
import os
import traceback
from md import md as MD
from firebase_admin import credentials, firestore
import random


class BaseManager:
    def __init__(self):
        try:
            self.cred = credentials.Certificate(os.path.join(os.path.dirname(
                __file__), "tfgforo-firebase-adminsdk-fbsvc-61fd334c13.json"))
            MASTER_KEY: Final[str] = os.getenv('MASTER_KEY')
            self.encripter = Encripter(MASTER_KEY.encode())
            if not firebase_admin._apps:
                firebase_admin.initialize_app(self.cred)
            self.db = firestore.client()
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

    # Esrte método es para obtener el md de de un usuario , basado en 2 emails , para encontrar el md de un usuario en concreto con el otro
    def _get_private_md(self, lista_users: list[str]) -> MD:
        try:
            user_ref = self.db.collection('md')
            user_ref_query = user_ref.where(
                filter=FieldFilter("users", 'array_contains_any', lista_users)).stream()
            for doc in user_ref_query:
                user_data = doc.to_dict()
                return MD(
                    id=user_data['id'],
                    usuario1=user_data['users'][0],
                    usuario2=user_data['users'][1]
                )
            return None
        except Exception as e:
            print(f"Error al obtener el md por email: {e}")
            return None

    # Vamos a hacer una función la cual toma un número n de usuarios que quiere devolver y una QUERY por la cual filtrar los usuarios, además de un campo por el que filtrar, para facilitar los algoritmos de búsqueda.
    def _get_users_by_algorithm(self, query,  field: str, current_user_email: str, limit: int = 3) -> list[User]:
        try:
            user_ref = self.db.collection('usuario')

            # Si query es una lista, usamos el operador 'in' para filtrar por múltiples valores

            if isinstance(query, list):
                user_ref_query = user_ref.where(filter=FieldFilter(
                    field, 'array_contains_any', query)).limit(limit)
            else:
                user_ref_query = user_ref.where(
                    field, '==', query).limit(limit).where("email", "!=", current_user_email).stream()

            docs = user_ref_query.stream()
            users = []
            print(user_ref_query)
            for doc in docs:
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
            traceback.print_exc()
            print(f"Error al obtener los usuarios por algoritmo: {e}")
            return []

    # Foro

    def _get_forums(self):
        from formularios.formularios import ForoModel
        try:

            foro_ref = self.db.collection('foro')
            foro_ref_query = foro_ref.stream()
            foros = []
            for doc in foro_ref_query:
                foro_data = doc.to_dict()

                mensajes_ref = doc.reference.collection('mensajes')
                mensajes_docs = mensajes_ref.stream()
                mensajes = [mensaje_doc.to_dict()
                            for mensaje_doc in mensajes_docs]

                # Crear una instancia de ForoModel con los datos obtenidos
                modelo_foro = ForoModel(
                    mensajes=mensajes,
                    descripcion=foro_data['Descripcion'],
                    dueño=foro_data['Dueño'],
                    titulo=foro_data['Tútulo'],
                    categorias=foro_data['categorias'],
                    fecha_creacion=foro_data['fecha_creacion'],
                    fecha_finalizacion=foro_data['fecha_finalizacion'],
                    fecha_modificado=foro_data['fecha_modificado'],
                    dueño_nickname=foro_data['dueño_nickname'],
                    dueñonombre=foro_data['dueñonombre'],
                    likes=foro_data['likes'],
                    comentarios=foro_data['comentarios'],
                )
                foros.append(modelo_foro)
            return foros
        except Exception as e:
            print(f"Error al obtener los foros: {e}")
            return None

    def get_forums_without_messages(self):
        from formularios.formularios import ForoModel
        try:
            foro_ref = self.db.collection('foro')
            foro_ref_query = foro_ref.order_by(
                'fecha_creacion', direction=firestore.Query.DESCENDING).limit(10).stream()
            foros = []
            for doc in foro_ref_query:
                foro_data = doc.to_dict()

                # Crear una instancia de ForoModel con los datos obtenidos
                modelo_foro = ForoModel(
                    id=doc.id,
                    mensajes=[],
                    descripcion=foro_data['Descripcion'],
                    dueño=foro_data['Dueño'],
                    titulo=foro_data['Tútulo'],
                    categorias=foro_data['categorias'],
                    fecha_creacion=foro_data['fecha_creacion'],
                    fecha_finalizacion=foro_data['fecha_finalizacion'],
                    fecha_modificado=foro_data['fecha_modificado'],
                    dueño_nickname=foro_data['dueño_nickname'],
                    dueñonombre=foro_data['dueñonombre'],
                    likes=foro_data['likes'],
                    comentarios=foro_data['comentarios'],
                )
                foros.append(modelo_foro)
            return foros
        except Exception as e:
            print(f"Error al obtener los foros: {e}")
            return None

    def get_messages_by_forum_id(self, foro_id: str) -> list[dict]:
        try:
            # Referencia al documento del foro
            foro_ref = self.db.collection('foro').document(foro_id)

            # Verificar si el documento del foro existe
            if not foro_ref.get().exists:
                raise ValueError(
                    f"No se encontró un foro con el ID: {foro_id}")

            # Obtener los mensajes de la subcolección 'mensajes'
            mensajes_ref = foro_ref.collection('mensajes')
            mensajes_docs = mensajes_ref.stream()

            # Convertir los documentos a un diccionario
            mensajes = [mensaje_doc.to_dict() for mensaje_doc in mensajes_docs]
            return mensajes
        except Exception as e:
            print(f"Error al obtener los mensajes del foro: {e}")
            return []

    def _add_forum(self, user: User, foro):
        from formularios.formularios import ForoModel
        try:
            # Para JUANAN
            # mensajes_foros es una  coleccion , la cuál vamos a meter dentro de un documeno de la coleccion foro
            # y dentro de la coleccion mensajes_foros vamos a meter los mensajes que se vayan añadiendo al foro
            # por lo que primeor creamos el documento de mensajes_foros y luego lo añadimos al documento de foro

            # Ejemplo de comoañadir un foro a la base de datos :
            """
            basemanager._add_forum(
                user=User.get(current_user.email),
                foro=ForoModel(
                    descripcion='Foro de prueba',
                    dueño=current_user.email,
                    titulo='Foro de prueba',
                    categorias=['programacion', 'python', 'flask'],
                    fecha_creacion=datetime.datetime.now(datetime.timezone.utc),
                    fecha_finalización=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7),
                    fecha_modificado=None
                )
            )
            """
            # Crear un nuevo documento en la colección 'foro'
            result = self.db.collection('foro').add({
                'Descripcion': foro.descripcion,
                'Dueño': user.email,
                'Tútulo': foro.titulo,
                'categorias': foro.categorias,
                'fecha_creacion': foro.fecha_creacion,
                'fecha_finalizacion': foro.fecha_finalizacion,
                'fecha_modificado': foro.fecha_modificado,
                'dueñonombre': user.nombre,
                'dueño_nickname': user.nickname,
                'likes': foro.likes,
                'comentarios': foro.comentarios,
                # 'mensajes_foro': mensajes_foro_ref,
            })
            foro_id = result[1].id
            print(f"Foro creado con ID: {foro_id}")
            return foro_id
        except Exception as e:
            print(f"Error al añadir el usuario: {e}")
            return False

    def _add_message_to_forum(self, id_foro: str, mensaje: str, user: User):
        from formularios.formularios import ForoModel

        # Ejemplo añadir un mensaje a un foro:
        """
        basemanager._add_message_to_forum(
            mensaje="Hola, soy un mensaje de prueba",
            id_foro="YXvJM25AVet9Jfp4ymeg",
            user=User.get(current_user.email)
        )
        """

        try:
            # Referencia al documento del foro
            foro_ref = self.db.collection('foro').document(id_foro)

            # Verificar si el documento del foro existe
            if not foro_ref.get().exists:
                raise ValueError(
                    f"No se encontró un foro con el ID: {id_foro}")

            # Agregar el mensaje a la subcolección 'mensajes' dentro del documento del foro
            foro_ref.collection('mensajes').add({
                'autor': user.nickname,
                'contenido': mensaje,
                'fecha': firestore.SERVER_TIMESTAMP
            })

            return True
        except Exception as e:
            print(f"Error al añadir el mensaje al foro: {e}")
            return False

    # def get_data_by_field(self, value) -> dict:
    #     try:
    #         users_query = self.db.collection("usuario").stream()
    #         posts_query = self.db.collection("foro").stream()

    #         usuarios = [doc.to_dict().get("nickname") for doc in users_query if value.lower(
    #         ) in doc.to_dict().get("nickname", "").lower()]
    #         posts = [doc.to_dict().get("Descripcion") for doc in posts_query if value.lower(
    #         ) in doc.to_dict().get("Descripcion", "").lower()]

    #         return {"usuarios": usuarios, "posts": posts}

    #     except Exception as e:
    #         print(f"Error en la búsqueda parcial: {e}")
    #         return {"usuarios": [], "posts": []}

    def get_data_by_field(self, value: str) -> dict:
        from formularios.formularios import ForoModel
        try:
            users_query = self.db.collection("usuario").stream()
            posts_query = self.db.collection("foro").stream()

            usuarios = []
            for doc in users_query:
                user_data = doc.to_dict()
                if value.lower() in user_data.get("nickname", "").lower():
                    usuario = User(
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
                    usuarios.append(usuario)
                    print(usuario)

            foros = []
            for doc in posts_query:
                foro_data = doc.to_dict()
                if value.lower() in foro_data.get("dueño_nickname", "").lower():
                    mensajes_ref = doc.reference.collection("mensajes")
                    mensajes_docs = mensajes_ref.stream()
                    mensajes = [mensaje_doc.to_dict()
                                for mensaje_doc in mensajes_docs]

                    modelo_foro = ForoModel(
                        mensajes=mensajes,
                        descripcion=foro_data['Descripcion'],
                        dueño=foro_data['Dueño'],
                        titulo=foro_data['Tútulo'],
                        categorias=foro_data['categorias'],
                        fecha_creacion=foro_data['fecha_creacion'],
                        fecha_finalizacion=foro_data['fecha_finalizacion'],
                        fecha_modificado=foro_data['fecha_modificado'],
                        dueño_nickname=foro_data['dueño_nickname'],
                        dueñonombre=foro_data['dueñonombre'],
                        likes=foro_data['likes'],
                        comentarios=foro_data['comentarios'],
                    )
                    foros.append(modelo_foro)
                    print(f" foro:{modelo_foro}")

            return {"usuarios": usuarios, "foros": foros}

        except Exception as e:
            print(f"Error en la búsqueda parcial: {e}")
            return {"usuarios": [], "foros": []}

    def get_user_by_nickname(self, nickname: str) -> User:
        try:
            user_ref = self.db.collection('usuario')
            user_ref_query = user_ref.where(
                'nickname', '==', nickname).stream()

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
            print(f"Error al obtener el usuario por nickname: {e}")
            return None

    def get_foros_by_user(self, nickname: str) -> list:
        from formularios.formularios import ForoModel
        try:
            posts_query = self.db.collection("foro").stream()

            foros = []
            for doc in posts_query:
                foro_data = doc.to_dict()
                if nickname.lower() in foro_data.get("dueño_nickname", "").lower():
                    mensajes_ref = doc.reference.collection("mensajes")
                    mensajes_docs = mensajes_ref.stream()
                    mensajes = [mensaje_doc.to_dict()
                                for mensaje_doc in mensajes_docs]

                    modelo_foro = ForoModel(
                        mensajes=mensajes,
                        descripcion=foro_data.get('Descripcion'),
                        dueño=foro_data.get('Dueño'),
                        titulo=foro_data.get('Tútulo'),
                        categorias=foro_data.get('categorias'),
                        fecha_creacion=foro_data.get('fecha_creacion'),
                        fecha_finalizacion=foro_data.get('fecha_finalizacion'),
                        fecha_modificado=foro_data.get('fecha_modificado'),
                        dueño_nickname=foro_data.get('dueño_nickname'),
                        dueñonombre=foro_data.get('dueñonombre'),
                        likes=foro_data.get('likes'),
                        comentarios=foro_data.get('comentarios'),
                        id=doc.id
                    )
                    foros.append(modelo_foro)

            return foros

        except Exception as e:
            print(f"Error al obtener los foros: {e}")
            return []
