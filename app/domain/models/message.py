from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class MensajeChat:
    id: Optional[int]
    id_cliente: int
    emisor: str
    contenido: str
    fecha: datetime