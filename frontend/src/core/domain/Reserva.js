export class Reserva {
    constructor({ id, cuarto_id, huesped_id, fecha_inicio, fecha_fin, estado }) {
        this.id = id; this.cuartoId = cuarto_id; this.huespedId = huesped_id;
        this.fechaInicio = fecha_inicio; this.fechaFin = fecha_fin; this.estado = estado;
    }
}