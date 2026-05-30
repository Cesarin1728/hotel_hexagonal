from dataclasses import dataclass
from typing import Optional

@dataclass
class Huesped:
    id: Optional[int]
    id_usuario: int 
    username: str
    clave: str
    miembro: bool
    economia: str
    edad: int