from dataclasses import dataclass
from typing import Optional

@dataclass
class Huesped:
    id: Optional[int]
    username: str
    clave: str
    miembro: bool
    economia: str
    edad: int