from dataclasses import dataclass 
from typing import Optional 

@dataclass 
class Cuarto: 
    id: Optional[int]  
    nombre: str   
    detalles: str   
    precio: int 
    espacio: str