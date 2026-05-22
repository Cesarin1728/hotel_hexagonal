from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models.cuarto import Cuarto

class CuartoRepository(ABC):

    @abstractmethod
    def create(self, c: Cuarto) -> Cuarto:
        pass

    @abstractmethod
    def get_all(self) -> List[Cuarto]:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Cuarto]:
        pass

    @abstractmethod
    def update(self, id: int, c: Cuarto) -> Cuarto:
        pass

    @abstractmethod
    def delete(self, id: int) -> None:
        pass