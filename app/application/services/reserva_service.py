# Nuestras aplicaciones. Nuestro servicio es ReservaService
# Nuestra lógica de negocio, donde está el uso real como crear una reserva o listar reservas
from typing import List, Optional   
from datetime import datetime    
from app.domain.models.reserva import Reserva                    
from app.domain.ports.reserva_repository import ReservaRepository  # el contrato que debe cumplir el repositorio

class ReservaService:

    def __init__(self, repository: ReservaRepository): # recibe una instancia del repositorio, en este caso para PostgreSQL con ReservaRepository
        self.repository = repository

        # crea la instancia con los datos recibidos. None en id porque la BD todavía no le asigna ID
    def create_reserva(self, espacio: str, fecha: datetime, servicio_cuarto: bool, noches: int, id_cuarto: int, id_huesped: int) -> Reserva:
        reserva = Reserva(id=None, espacio=espacio, fecha=fecha, servicio_cuarto=servicio_cuarto, noches=noches, id_cuarto=id_cuarto, id_huesped=id_huesped)
        return self.repository.create(reserva)

    def list_reservas(self) -> List[Reserva]:
        return self.repository.get_all()

    def get_reserva(self, id: int) -> Optional[Reserva]:
        return self.repository.get_by_id(id)

    def get_reservas_por_huesped(self, id_huesped: int) -> List[Reserva]:
        return self.repository.get_by_huesped(id_huesped)

    def update_reserva(self, id: int, espacio: str, fecha: datetime, servicio_cuarto: bool, noches: int, id_cuarto: int, id_huesped: int) -> Reserva:
        reserva = Reserva(id=id, espacio=espacio, fecha=fecha, servicio_cuarto=servicio_cuarto, noches=noches, id_cuarto=id_cuarto, id_huesped=id_huesped)
        return self.repository.update(id, reserva)

    def delete_reserva(self, id: int) -> None:
        return self.repository.delete(id)