import { Reserva } from '../../core/domain/Reserva.js';
export class ReservaApiAdapter {
    constructor(baseUrl) { this.baseUrl = baseUrl; }
    async crearReserva(datosReserva, token) {
        const res = await fetch(`${this.baseUrl}/api/reservas/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
            body: JSON.stringify(datosReserva)
        });
        if (!res.ok) throw new Error("Error en reserva");
        return new Reserva(await res.json());
    }
    async listarTodas(token) {
        const res = await fetch(`${this.baseUrl}/api/reservas/`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const data = await res.json();
        return data.map(item => new Reserva(item));
    }
}