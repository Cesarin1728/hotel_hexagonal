from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.infrastructure.security.jwt_manager import JWTManager

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
jwt_manager   = JWTManager()

def obtener_usuario_actual(token: str = Depends(oauth2_scheme)) -> dict:
    payload = jwt_manager.decode_token(token)
    if not payload or payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Token inválido o expirado", headers={"WWW-Authenticate": "Bearer"})
    return payload

def requerir_admin(usuario: dict = Depends(obtener_usuario_actual)) -> dict:
    if usuario.get("rol") != "Administrador":
        raise HTTPException(status_code=403, detail="Acceso denegado: se requiere rol Administrador")
    return usuario