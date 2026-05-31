import { Cuarto } from '../../core/domain/Cuarto.js';
export class CuartoApiAdapter {
    constructor(baseUrl) { this.baseUrl = baseUrl; }
    async listarTodos() {
        const res = await fetch(`${this.baseUrl}/api/cuartos/`);
        const data = await res.json();
        return data.map(item => new Cuarto(item));
    }
    async crear(datosCuarto, imagenFile, token) {
        const formData = new FormData();
        formData.append('nombre', datosCuarto.nombre);
        formData.append('detalles', datosCuarto.detalles);
        formData.append('precio', datosCuarto.precio);
        formData.append('espacio', datosCuarto.espacio);
        formData.append('imagen', imagenFile);

        const res = await fetch(`${this.baseUrl}/api/cuartos/`, {
            method: 'POST', headers: { 'Authorization': `Bearer ${token}` }, body: formData
        });
        if (!res.ok) throw new Error("Error al crear el cuarto");
        return new Cuarto(await res.json());
    }
}