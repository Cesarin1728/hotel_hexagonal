# Nuestro dominio, representa la entidad reserca. Solo son datos puros

from dataclasses import dataclass  # dataclass es una forma rápida de crear clases que solo guardan datos. En este caso cumple para hacer nuestro dominio 
from typing import Optional 
from datetime import datetime

@dataclass  # esta clase es solo para guardar datos. Es el dominio, no sabe nada de BD ni FastAPI
class Reserva:
    id: Optional[int]        # None al crear, la BD asigna el ID después. Optional porque puede ser None, pero una vez creada la reserva ya tendrá un ID
    espacio: str
    fecha: datetime
    servicio_cuarto: bool 
    noches: int 
    id_cuarto: int 
    id_huesped: int