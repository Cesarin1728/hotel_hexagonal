from pydantic import BaseModel

class HuespedRequest(BaseModel):
    username: str
    clave: str
    miembro: bool
    economia: str
    edad: int

class HuespedResponse(BaseModel):
    id: int
    username: str
    miembro: bool
    economia: str
    edad: int