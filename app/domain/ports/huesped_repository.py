from abc import ABC, abstractmethod  
from typing import List, Optional   
from app.domain.models.huesped import Huesped 

class HuespedRepository(ABC): 
    
    @abstractmethod 
    def create(self, h: Huesped) -> Huesped: 
        pass

    @abstractmethod
    def get_all(self) -> List[Huesped]: 
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Huesped]: 
        pass

    @abstractmethod
    def update(self, id: int, h: Huesped) -> Huesped: 
        pass

    @abstractmethod
    def delete(self, id: int) -> None:
        pass