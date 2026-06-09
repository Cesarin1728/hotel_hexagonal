import { Reserva } from '../../core/domain/Reserva.js';

export class ReservaApiAdapter {
    constructor(baseUrl) { this.baseUrl = baseUrl; }

    async crearReserva(datosReserva, token) {
        const response = await fetch(`${this.baseUrl}/api/reservas/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(datosReserva)
        });
        if (!response.ok) throw new Error("Error en reserva");
        return new Reserva(await response.json());
    }

    async listarTodas(token) {
        const response = await fetch(`${this.baseUrl}/api/reservas/`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!response.ok) throw new Error("No autorizado");
        const data = await response.json();
        return data.map(item => new Reserva(item));
    }

    async listarPorHuesped(id_huesped, token) {
        const response = await fetch(`${this.baseUrl}/api/reservas/huesped/${id_huesped}`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!response.ok) throw new Error("Error al obtener tu historial");
        const data = await response.json();
        return data.map(item => new Reserva(item));
    }
}