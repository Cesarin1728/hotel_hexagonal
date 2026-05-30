from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.application.services.chat_service import ChatService
from app.infrastructure.faq.faq_memory_repository import InMemoryFAQRepository

router = APIRouter(prefix="/ws", tags=["Chat Realtime"])

# Inyección de dependencias manual (Conectamos la infraestructura con el servicio)
faq_repo = InMemoryFAQRepository()
chat_service = ChatService(faq_repo)

@router.websocket("/chat/{user}")
async def websocket_chat(websocket: WebSocket, user: str):
    await websocket.accept() # Aceptamos la conexión HTTP y hacemos el Upgrade a WebSocket
    await websocket.send_text(f"Bienvenido al asistente del Hotel {user}")
    
    try:
        while True:
            # Esperamos el mensaje del cliente de forma asíncrona
            data = await websocket.receive_text()
            
            # Pasamos el mensaje por nuestro caso de uso
            respuesta = chat_service.process_message(user, data)
            
            # Devolvemos la respuesta al cliente
            await websocket.send_text(f"Asistente: {respuesta}")
            
    except WebSocketDisconnect:
        print(f"El usuario {user} se ha desconectado del chat.")