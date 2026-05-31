from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
import json
from app.application.services.chat_service import ChatService
from app.infrastructure.faq.faq_memory_repository import InMemoryFAQRepository
from app.infrastructure.db.mysql.mensaje_repo import PostgresMensajeRepository
# 1. Importamos la clase correcta
from app.infrastructure.security.jwt_manager import JWTManager 

router = APIRouter(prefix="/ws", tags=["Chat Realtime"])

faq_repo = InMemoryFAQRepository()
msg_repo = PostgresMensajeRepository()
chat_service = ChatService(faq_repo, msg_repo)
jwt_manager = JWTManager() 

class ConnectionManager:
    def __init__(self):
        self.active_clients: dict[int, WebSocket] = {} 
        self.admin_ws: WebSocket = None 

    async def connect_client(self, id_cliente: int, websocket: WebSocket):
        await websocket.accept()
        self.active_clients[id_cliente] = websocket

    async def connect_admin(self, websocket: WebSocket):
        await websocket.accept()
        self.admin_ws = websocket

    def disconnect_client(self, id_cliente: int):
        if id_cliente in self.active_clients:
            del self.active_clients[id_cliente]

    def disconnect_admin(self):
        self.admin_ws = None

    async def send_to_admin(self, id_cliente: int, mensaje: str):
        if self.admin_ws:
            await self.admin_ws.send_text(json.dumps({"id_cliente": id_cliente, "msg": f"Cliente {id_cliente}: {mensaje}"}))

    async def send_to_client(self, id_cliente: int, mensaje: str):
        if id_cliente in self.active_clients:
            await self.active_clients[id_cliente].send_text(f"Admin: {mensaje}")

manager = ConnectionManager()

@router.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket, token: str):
    payload = jwt_manager.decode_token(token)
    
    if not payload:
        await websocket.close(code=1008)
        return

    usuario_id = payload.get("id")
    rol = payload.get("rol")

    if rol == "Administrador":
        await manager.connect_admin(websocket)
        await websocket.send_text(json.dumps({"msg": "Conectado como Administrador. Esperando consultas..."}))
        try:
            while True:
                data = await websocket.receive_text()
                json_data = json.loads(data)
                
                target_cliente = int(json_data["id_cliente"])
                respuesta_admin = json_data["msg"]

                chat_service.guardar_mensaje_admin(target_cliente, respuesta_admin)
                await manager.send_to_client(target_cliente, respuesta_admin)
        except WebSocketDisconnect:
            manager.disconnect_admin()

    elif rol == "Cliente":
        await manager.connect_client(usuario_id, websocket)
        
        historial = chat_service.obtener_historial(usuario_id)
        for h in historial:
            await websocket.send_text(f"{h.emisor}: {h.contenido}")
            
        try:
            while True:
                data = await websocket.receive_text()
                bot_response = chat_service.procesar_mensaje_cliente(usuario_id, data)
                
                if bot_response:
                    await websocket.send_text(f"Bot: {bot_response}")
                else:
                    await websocket.send_text("Bot: Un administrador revisará tu consulta en breve...")
                    await manager.send_to_admin(usuario_id, data)
                    
        except WebSocketDisconnect:
            manager.disconnect_client(usuario_id)