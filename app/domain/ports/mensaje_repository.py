from abc import ABC, abstractmethod
from typing import List
from app.domain.models.message import MensajeChat

class MensajeRepository(ABC):
    @abstractmethod
    def guardar(self, mensaje: MensajeChat) -> MensajeChat:
        pass

    @abstractmethod
    def obtener_historial(self, id_cliente: int) -> List[MensajeChat]:
        pass