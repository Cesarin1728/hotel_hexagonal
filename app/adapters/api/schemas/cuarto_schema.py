from pydantic import BaseModel
from typing import Optional

class CuartoRequest(BaseModel):
    nombre: str
    detalles: str
    precio: int
    espacio: str

class CuartoResponse(BaseModel):
    id: int
    nombre: str
    detalles: str
    precio: int
    espacio: str
    imagen_url: Optional[str] = None