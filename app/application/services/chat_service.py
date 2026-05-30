from datetime import datetime
from app.domain.models.message import MensajeChat
from app.domain.ports.faq_port import FAQPort
from app.domain.ports.mensaje_repository import MensajeRepository

class ChatService:
    def __init__(self, faq_repository: FAQPort, mensaje_repository: MensajeRepository):
        self.faq_repository = faq_repository
        self.mensaje_repository = mensaje_repository

    def obtener_historial(self, id_cliente: int):
        return self.mensaje_repository.obtener_historial(id_cliente)

    def procesar_mensaje_cliente(self, id_cliente: int, contenido: str):
        msg_cliente = MensajeChat(id=None, id_cliente=id_cliente, emisor="Cliente", contenido=contenido, fecha=datetime.now())
        self.mensaje_repository.guardar(msg_cliente)

        respuesta_bot = self.faq_repository.get_answer(contenido)
        
        if respuesta_bot != "No tengo una respuesta automatizada para eso.":
            msg_bot = MensajeChat(id=None, id_cliente=id_cliente, emisor="Bot", contenido=respuesta_bot, fecha=datetime.now())
            self.mensaje_repository.guardar(msg_bot)
            return respuesta_bot
            
        return None

    def guardar_mensaje_admin(self, id_cliente: int, contenido: str):
        msg_admin = MensajeChat(id=None, id_cliente=id_cliente, emisor="Administrador", contenido=contenido, fecha=datetime.now())
        self.mensaje_repository.guardar(msg_admin)