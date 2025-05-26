from flask_socketio import SocketIO
from BaseManager import BaseManager

socketio = SocketIO()

def get_messages(id):
    return BaseManager().get_messages_by_forum_id(id)