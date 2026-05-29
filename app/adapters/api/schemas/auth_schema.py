from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreateRequest(BaseModel):
    email: EmailStr
    password: str
    rol: Optional[str] = "Cliente"

class RefreshRequest(BaseModel):
    refresh_token: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str

class UsuarioResponse(BaseModel):
    id: int
    email: str
    rol: str