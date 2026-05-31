export class Reserva {
    constructor({ id, espacio, fecha, servicio_cuarto, noches, costo, id_cuarto, id_huesped }) {
        this.id = id;
        this.espacio = espacio;
        this.fecha = fecha;
        this.servicioCuarto = servicio_cuarto;
        this.noches = noches;
        this.costo = costo;
        this.cuartoId = id_cuarto; 
        this.huespedId = id_huesped;
    }
}