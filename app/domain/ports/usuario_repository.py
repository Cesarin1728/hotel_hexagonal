from abc import ABC, abstractmethod
from typing import Optional
from app.domain.models.usuario import Usuario

class UsuarioRepository(ABC):
    @abstractmethod
    def create(self, u: Usuario) -> Usuario:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Usuario]:
        pass

    @abstractmethod
    def delete(self, id: int) -> None:
        pass