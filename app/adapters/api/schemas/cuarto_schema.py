from pydantic import BaseModel

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