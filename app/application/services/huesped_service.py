from typing import List, Optional
from app.domain.models.huesped import Huesped
from app.domain.ports.huesped_repository import HuespedRepository
from fastapi import HTTPException

class HuespedService:

    def __init__(self, repository: HuespedRepository):
        self.repository = repository

    def create_huesped(self, username: str, clave: str, miembro: bool, economia: str, edad: int) -> Huesped:
        if edad <= 0:
            raise HTTPException(status_code=400, detail="La edad no puede ser negativa")

        huesped = Huesped(id=None, username=username, clave=clave, miembro=miembro, economia=economia, edad=edad)
        return self.repository.create(huesped)

    def list_huespedes(self) -> List[Huesped]:
        return self.repository.get_all()

    def get_huesped(self, id: int) -> Optional[Huesped]:
        return self.repository.get_by_id(id)

    def update_huesped(self, id: int, username: str, clave: str, miembro: bool, economia: str, edad: int) -> Huesped:
        if edad <= 0:
            raise HTTPException(status_code=400, detail="La edad no puede ser negativa")

        huesped = Huesped(id=id, username=username, clave=clave, miembro=miembro, economia=economia, edad=edad)
        return self.repository.update(id, huesped)

    def delete_huesped(self, id: int) -> None:
        return self.repository.delete(id)