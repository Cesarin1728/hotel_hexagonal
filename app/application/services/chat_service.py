from datetime import datetime
from app.domain.models.message import Message
from app.domain.ports.faq_port import FAQPort

class ChatService:
    def __init__(self, faq_repository: FAQPort):
        self.faq_repository = faq_repository

    def process_message(self, user: str, content: str) -> str:
        # 1. Creamos la entidad del mensaje (si en el futuro quieres guardarlos en BD)
        message = Message(id=None, user=user, content=content, created_at=datetime.now())
        
        # 2. Consultamos al puerto (nuestro proveedor de FAQ)
        respuesta = self.faq_repository.get_answer(message.content)
        return respuesta