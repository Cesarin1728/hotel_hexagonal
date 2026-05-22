from typing import List, Optional
from app.domain.models.cuarto import Cuarto
from app.domain.ports.cuarto_repository import CuartoRepository

class CuartoService:

    def __init__(self, repository: CuartoRepository):
        self.repository = repository

    def create_cuarto(self, nombre: str, detalles: str, precio: int, espacio: str) -> Cuarto:
        cuarto = Cuarto(id=None, nombre=nombre, detalles=detalles, precio=precio, espacio=espacio)
        return self.repository.create(cuarto)

    def list_cuartos(self) -> List[Cuarto]:
        return self.repository.get_all()

    def get_cuarto(self, id: int) -> Optional[Cuarto]:
        return self.repository.get_by_id(id)

    def update_cuarto(self, id: int, nombre: str, detalles: str, precio: int, espacio: str) -> Cuarto:
        cuarto = Cuarto(id=id, nombre=nombre, detalles=detalles, precio=precio, espacio=espacio)
        return self.repository.update(id, cuarto)

    def delete_cuarto(self, id: int) -> None:
        return self.repository.delete(id)