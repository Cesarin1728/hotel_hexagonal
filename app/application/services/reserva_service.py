# Nuestras aplicaciones. Nuestro servicio es ReservaService
# Nuestra lógica de negocio, donde está el uso real como crear una reserva o listar reservas
from typing import List, Optional   
from datetime import datetime, timedelta    
from app.domain.models.reserva import Reserva                    
from app.domain.ports.reserva_repository import ReservaRepository
from app.domain.ports.cuarto_repository import CuartoRepository
from app.domain.ports.huesped_repository import HuespedRepository
from fastapi import HTTPException

class ReservaService:

    def __init__(self, repository: ReservaRepository, cuarto_repository: CuartoRepository, huesped_repository: HuespedRepository):
        self.repository = repository
        self.cuarto_repository = cuarto_repository
        self.huesped_repository = huesped_repository

        # crea la instancia con los datos recibidos. None en id porque la BD todavía no le asigna ID
    def create_reserva(self, espacio: str, fecha: datetime, servicio_cuarto: bool, noches: int, id_cuarto: int, id_huesped: int) -> Reserva:
        
        if noches <= 0:
            raise HTTPException(status_code=400, detail="No hay noches negativas we")

        huesped = self.huesped_repository.get_by_id(id_huesped)
        if not huesped:
            raise HTTPException(status_code=404, detail=f"El huesped {id_huesped} no existe")

        cuarto = self.cuarto_repository.get_by_id(id_cuarto)
        if not cuarto:
            raise HTTPException(status_code=404, detail=f"El cuarto {id_cuarto} no existe")

        nueva_fecha_inicio = fecha
        nueva_fecha_fin = fecha + timedelta(days=noches)

        todas_las_reservas = self.repository.get_all()
        for r in todas_las_reservas:
            if r.id_cuarto == id_cuarto:
                existente_inicio = r.fecha
                existente_fin = r.fecha + timedelta(days=r.noches)

                if nueva_fecha_inicio < existente_fin and nueva_fecha_fin > existente_inicio:
                    raise HTTPException(
                        status_code=400, 
                        detail=f"El cuarto {id_cuarto} ya está ocupado desde el {existente_inicio.strftime('%Y-%m-%d %H:%M')} hasta el {existente_fin.strftime('%Y-%m-%d %H:%M')}."
                    )

        costo = cuarto.precio * noches

        reserva = Reserva(id=None, espacio=espacio, fecha=fecha, servicio_cuarto=servicio_cuarto,
                          noches=noches, costo=costo, id_cuarto=id_cuarto, id_huesped=id_huesped)
        return self.repository.create(reserva)

    def list_reservas(self) -> List[Reserva]:
        return self.repository.get_all() 

    def get_reserva(self, id: int) -> Optional[Reserva]:
        return self.repository.get_by_id(id)

    def get_reservas_por_huesped(self, id_huesped: int) -> List[Reserva]:
        return self.repository.get_by_huesped(id_huesped)

    def update_reserva(self, id: int, espacio: str, fecha: datetime, servicio_cuarto: bool, noches: int, id_cuarto: int, id_huesped: int) -> Reserva:
        
        if noches <= 0:
            raise HTTPException(status_code=400, detail="La cantidad de noches debe ser mayor a cero.")

        if not self.huesped_repository.get_by_id(id_huesped):
            raise HTTPException(status_code=404, detail=f"El huesped {id_huesped} no existe.")
            
        cuarto = self.cuarto_repository.get_by_id(id_cuarto)
        if not cuarto:
            raise HTTPException(status_code=404, detail=f"El cuarto {id_cuarto} no existe.")

        nueva_fecha_inicio = fecha
        nueva_fecha_fin = fecha + timedelta(days=noches)

        todas_las_reservas = self.repository.get_all()
        for r in todas_las_reservas:
            if r.id_cuarto == id_cuarto and r.id != id:
                existente_inicio = r.fecha
                existente_fin = r.fecha + timedelta(days=r.noches)

                if nueva_fecha_inicio < existente_fin and nueva_fecha_fin > existente_inicio:
                    raise HTTPException(
                        status_code=400, 
                        detail=f"El cuarto {id_cuarto} ya está ocupado desde  {existente_inicio.strftime('%Y-%m-%d %H:%M')} al {existente_fin.strftime('%Y-%m-%d %H:%M')}."
                    )

        costo = cuarto.precio * noches

        reserva = Reserva(id=id, espacio=espacio, fecha=fecha, servicio_cuarto=servicio_cuarto,
                          noches=noches, costo=costo, id_cuarto=id_cuarto, id_huesped=id_huesped)
        return self.repository.update(id, reserva)

    def delete_reserva(self, id: int) -> None:
        return self.repository.delete(id)