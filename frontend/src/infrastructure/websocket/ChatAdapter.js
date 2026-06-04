export class ChatAdapter {
    constructor(wsUrl) { 
        this.wsUrl = wsUrl; 
        this.socket = null; 
    }
    
    conectar(token, onMensajeRecibido) {
        this.socket = new WebSocket(`${this.wsUrl}/ws/chat?token=${token}`);
        this.socket.onmessage = (event) => onMensajeRecibido(event.data);
    }
    
    enviarMensaje(mensaje) {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            this.socket.send(mensaje);
        }
    }
}