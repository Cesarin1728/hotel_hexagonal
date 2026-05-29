from dataclasses import dataclass
from typing import Optional

@dataclass
class Usuario:
    id: Optional[int]
    email: str          
    password_hash: str  
    rol: str