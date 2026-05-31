export class ChatAdapter {
    constructor(wsUrl) { this.wsUrl = wsUrl; this.socket = null; }
    conectar(rol, onMensajeRecibido) {
        this.socket = new WebSocket(`${this.wsUrl}/api/chat/ws/${rol}`);
        this.socket.onmessage = (event) => onMensajeRecibido(event.data);
    }
    enviarMensaje(mensaje) {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) this.socket.send(mensaje);
    }
}