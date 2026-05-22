# Es nuestro puerto, son interfaces que defininen qué cosas se pueden hacer, pero no cómo se hacen. Por eso son métodos abstractos
from abc import ABC, abstractmethod  #Para definir las interfaces (nuestros contratos) y forzar a su cumplimiento
from typing import List, Optional   
from app.domain.models.reserva import Reserva  # importa el modelo del dominio

class ReservaRepository(ABC):

    @abstractmethod 
    def create(self, r: Reserva) -> Reserva: # Crear función en phtyon es def nombre_funcion(parametros) -> tipo_retorno
        pass  # sin lógica, solo solo lo que va a hacer, pero no cómo

    @abstractmethod
    def get_all(self) -> List[Reserva]:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Reserva]:
        pass

    @abstractmethod
    def get_by_huesped(self, id_huesped: int) -> List[Reserva]:
        pass

    @abstractmethod
    def update(self, id: int, r: Reserva) -> Reserva:
        pass

    @abstractmethod
    def delete(self, id: int) -> None:
        pass