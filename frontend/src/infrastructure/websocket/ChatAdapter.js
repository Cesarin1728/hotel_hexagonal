export class ChatAdapter {
    constructor(wsUrl) { 
        this.wsUrl = wsUrl; 
        this.socket = null; 
    }
    
    // Ahora recibe el token en lugar de un 'rol' quemado
    conectar(token, onMensajeRecibido) {
        // La URL debe coincidir con el @router.websocket("/chat") de tu chat_router.py
        this.socket = new WebSocket(`${this.wsUrl}/ws/chat?token=${token}`);
        this.socket.onmessage = (event) => onMensajeRecibido(event.data);
    }
    
    enviarMensaje(mensaje) {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            // El backend espera un JSON con la estructura que definiste en chat_router.py
            this.socket.send(mensaje);
        }
    }
}